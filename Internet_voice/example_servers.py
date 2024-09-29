import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from vosk import Model, KaldiRecognizer
import json
import threading
import telebot
import janus  # Import janus for thread-safe queues

app = FastAPI()

# Load Vosk model
try:
    model = Model("D://Coding_AI//Internet_voice//model//")
    logging.info("Vosk model loaded successfully.")
except Exception as e:
    logging.error(f"Could not load Vosk model: {e}")

# Telegram Bot setup
bot_token = "7238562180:AAGt88x25LzLTBnoxzVEj8kGmGWXybzxyZg"  # Replace with your Telegram bot token
bot = telebot.TeleBot(bot_token)
bot.remove_webhook()

# Define global variables for the queues, to be initialized later
telegram_message_queue = None
http_message_queue = None
tcp_message_queue = None
audio_transcription_queue = None
client_response_queue = None

# Start the Telebot in a separate thread
def start_telebot():
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, "Howdy, how are you doing?")

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        # Put the message text into the queue
        telegram_message_queue.sync_q.put(message.text)
        bot.reply_to(message, f"Received your message: {message.text}")

    bot.infinity_polling()

telebot_thread = threading.Thread(target=start_telebot, daemon=True)
telebot_thread.start()

# Graceful shutdown
@app.on_event("shutdown")
def shutdown_event():
    bot.stop_polling()
    logging.info("Stopping Telebot polling...")
    if telebot_thread.is_alive():
        telebot_thread.join()
    logging.info("Telebot thread stopped.")

# TCP server to receive data on port 5002
async def start_tcp_server():
    async def handle_client(reader, writer):
        try:
            data = await reader.read(10000)  # Adjust buffer size as needed
            message = data.decode()
            tcp_message_queue.sync_q.put(message)
            writer.write(b"Message received")
            await writer.drain()
        except Exception as e:
            logging.error(f"Error in TCP client handler: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_server(handle_client, '0.0.0.0', 5002)
    logging.info("TCP server started on port 5002")

    async with server:
        await server.serve_forever()

# Initialize queues and start background tasks on startup
@app.on_event("startup")
async def startup_event():
    global telegram_message_queue, http_message_queue, tcp_message_queue, audio_transcription_queue, client_response_queue
    # Initialize the queues here, when the event loop is running
    telegram_message_queue = janus.Queue()
    http_message_queue = janus.Queue()
    tcp_message_queue = janus.Queue()
    audio_transcription_queue = janus.Queue()
    client_response_queue = janus.Queue()
    # Start the TCP server and the message handler
    asyncio.create_task(start_tcp_server())
    asyncio.create_task(handle_all_messages())

# HTTP endpoint to receive data
@app.post("/receive_data")
async def receive_data(request: Request):
    data = await request.json()
    message = data.get('message')
    if message:
        http_message_queue.sync_q.put(message)
        return {"status": "success"}
    else:
        return {"status": "failure", "reason": "No message provided"}

# Global set of connected WebSocket clients
connected_websockets = set()

# Background task to handle all messages
async def handle_all_messages():
    try:
        while True:
            # Wait for any message from the queues
            tasks = [
                asyncio.create_task(telegram_message_queue.async_q.get()),
                asyncio.create_task(http_message_queue.async_q.get()),
                asyncio.create_task(tcp_message_queue.async_q.get()),
                asyncio.create_task(audio_transcription_queue.async_q.get()),
            ]
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                message = task.result()
                # Process the message as needed
                logging.info(f"Processing message: {message}")
                # Send the message to all connected WebSocket clients
                for websocket in connected_websockets.copy():
                    try:
                        await websocket.send_text(f"Server Message: {message}")
                    except WebSocketDisconnect:
                        connected_websockets.remove(websocket)
                    except Exception as e:
                        logging.error(f"Error sending message to client: {e}")
            for task in pending:
                task.cancel()
    except Exception as e:
        logging.error(f"Error in handle_all_messages: {e}")

@app.websocket("/TranscribeStreaming")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)
    recognizer = KaldiRecognizer(model, 16000)
    audio_queue = asyncio.Queue()

    try:
        # Task to receive messages from the client (both audio and text)
        async def receive_messages():
            try:
                while True:
                    message = await websocket.receive()
                    if "bytes" in message:
                        audio_chunk = message["bytes"]
                        await audio_queue.put(audio_chunk)
                    elif "text" in message:
                        text_message = message["text"]
                        logging.info(f"Received text message from client: {text_message}")
                        if text_message == "submit_response":
                            # Signal to stop the audio stream
                            await audio_queue.put(None)
                            break
                        else:
                            # Handle client responses
                            client_response_queue.sync_q.put(text_message)
            except WebSocketDisconnect:
                logging.info("WebSocket disconnected in receive_messages")
            except Exception as e:
                logging.error(f"Error in receive_messages: {e}")

        # Task to process audio data and perform speech recognition
        async def process_audio():
            try:
                while True:
                    audio_chunk = await audio_queue.get()
                    if audio_chunk is None:
                        break  # End of stream
                    if recognizer.AcceptWaveform(audio_chunk):
                        result = recognizer.Result()
                        result_json = json.loads(result)
                        text = result_json.get('text', '')
                        if text:
                            audio_transcription_queue.sync_q.put(text)
                            await websocket.send_text(f"Transcription: {text}")
                    else:
                        partial_result = recognizer.PartialResult()
                        result_json = json.loads(partial_result)
                        text = result_json.get('partial', '')
                        if text:
                            await websocket.send_text(f"Partial: {text}")
                # Send final result
                final_result = recognizer.FinalResult()
                result_json = json.loads(final_result)
                text = result_json.get('text', '')
                if text:
                    audio_transcription_queue.sync_q.put(text)
                    await websocket.send_text(f"Final Transcription: {text}")
            except Exception as e:
                logging.error(f"Error in process_audio: {e}")

        receive_task = asyncio.create_task(receive_messages())
        process_task = asyncio.create_task(process_audio())
        await asyncio.gather(receive_task, process_task)
    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        connected_websockets.discard(websocket)
        await websocket.close()

if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO)

    def run():
        uvicorn.run(app, host="0.0.0.0", port=8000, ws_ping_interval=None)

    try:
        run()
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
