import openwakeword
from openwakeword.model import Model
openwakeword.utils.download_models()
import asyncio
import websockets
import sounddevice as sd
import time
import soundfile

time_past = time.time()
# Initialize the OpenWakeWord model
owwModel = Model(inference_framework="onnx")  # onnx or tflite
thread_activate = True
send_data = True

async def send_audio(ws):
    """Send audio data to WebSocket server only if wake word is detected."""
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()
    wakeword_detected = False

    def audio_callback(indata, frames, time_data, status):
        global thread_activate
        global time_past
        global send_data
        try:
            audio_data = indata[:, 0]
            owwModel.predict(audio_data)

            for mdl in owwModel.prediction_buffer.keys():
                if mdl == "alexa": # Say "Alexa" to activate
                    scores = list(owwModel.prediction_buffer[mdl])
                    if scores[-1] <= 0.5:
                        thread_activate = True
                    else:
                        if thread_activate:
                            print("Wake word detected!")
                            thread_activate = False
                            send_data = True
                            time_past = time.time()

            if send_data:
                loop.call_soon_threadsafe(input_queue.put_nowait, indata.tobytes())
            if (time.time() - time_past) > 10:
                send_data = False

        except Exception as e:
            print(f"Error in audio_callback: {e}")

    # Record audio stream
    stream = sd.InputStream(channels=1, samplerate=16000, dtype='int16', callback=audio_callback, blocksize=1600)  # Adjust blocksize as needed

    # Send audio stream to the server
    with stream:
        print("Recording audio. Press Ctrl+C to stop.")
        try:
            while True:
                indata = await input_queue.get()
                await ws.send(indata)
        except asyncio.CancelledError:
            pass
        except KeyboardInterrupt:
            pass
        finally:
            # Signal end of audio stream
            await ws.send("submit_response")
            await ws.close()  # Explicitly close the WebSocket connection

async def receive_transcriptions(ws, assistant_ws):
    """Receive transcriptions from WebSocket server and send them to the assistant."""
    try:
        async for message in ws:
            print(f"Received transcription: {message}")
            # Send the transcribed text to assistant
            await assistant_ws.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed with transcription server.")

async def send_text(assistant_ws):
    """Send text messages to Assistant WebSocket server."""
    loop = asyncio.get_event_loop()
    while True:
        try:
            text = await loop.run_in_executor(None, input, "> ")
            await assistant_ws.send(text)
            if text.lower() == "exit":
                break
        except asyncio.CancelledError:
            break

async def receive_responses(assistant_ws):
    """Receive responses from assistant."""
    try:
        async for message in assistant_ws:
            print(f"Assistant says: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed with assistant.")

async def connect_and_run():
    """Try to connect to the WebSocket servers and run the main logic, retry on failure."""
    audio_uri = "ws://localhost:8000/TranscribeStreaming"  # Transcription server
    assistant_uri = "ws://localhost:8001"  # Assistant server

    while True:
        try:
            async with websockets.connect(audio_uri) as audio_ws, websockets.connect(assistant_uri) as assistant_ws:
                # Start tasks
                send_audio_task = asyncio.create_task(send_audio(audio_ws))
                receive_transcription_task = asyncio.create_task(receive_transcriptions(audio_ws, assistant_ws))
                send_text_task = asyncio.create_task(send_text(assistant_ws))
                receive_response_task = asyncio.create_task(receive_responses(assistant_ws))

                # Wait for tasks to complete
                await asyncio.gather(send_audio_task, receive_transcription_task, send_text_task, receive_response_task)
        except (websockets.exceptions.InvalidURI, websockets.exceptions.ConnectionClosedError, ConnectionRefusedError):
            print("Unable to connect to the WebSocket servers. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(connect_and_run())
