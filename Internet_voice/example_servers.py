import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from vosk import Model, KaldiRecognizer
import json
import uvicorn
import websockets

app = FastAPI()

# Load Vosk model
try:
    model = Model(r"D:\Voice-Assistant\Internet_voice\model")  # Replace with your model path
    logging.info("Vosk model loaded successfully.")
except Exception as e:
    logging.error(f"Could not load Vosk model: {e}")

async def send_to_assistant(message):
    uri = "ws://localhost:8001"  # Assistant's WebSocket
    try:
        async with websockets.connect(uri) as ws:
            await ws.send(message)
            # Optionally, receive response from assistant
            async for response in ws:
                print(f"Assistant response: {response}")
                break  # Assuming we only want the first response
    except Exception as e:
        logging.error(f"Error sending to assistant: {e}")

@app.websocket("/TranscribeStreaming")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    recognizer = KaldiRecognizer(model, 16000)
    try:
        while True:
            data = await websocket.receive_bytes()
            if data == b"submit_response":
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_json = json.loads(result)
                text = result_json.get('text', '')
                if text:
                    # Send the transcription to the assistant
                    await send_to_assistant(text)
                    # Also send back to the robot if needed
                    await websocket.send_text(text)
            else:
                # Partial result if needed
                pass
        # Send final result
        final_result = recognizer.FinalResult()
        result_json = json.loads(final_result)
        text = result_json.get('text', '')
        if text:
            await send_to_assistant(text)
            await websocket.send_text(text)
    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    def run():
        uvicorn.run(app, host="0.0.0.0", port=8000, ws_ping_interval=None)

    try:
        run()
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
