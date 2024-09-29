import asyncio
import websockets
import sounddevice as sd

async def send_audio(ws):
    """Send audio data to WebSocket server."""
    loop = asyncio.get_event_loop()
    input_queue = asyncio.Queue()

    def audio_callback(indata, frames, time, status):
        loop.call_soon_threadsafe(input_queue.put_nowait, indata.tobytes())

    # Record audio stream
    stream = sd.InputStream(
        channels=1,
        samplerate=16000,
        dtype='int16',
        callback=audio_callback,
        blocksize=1600  # Adjust blocksize as needed
    )

    # Send audio stream to the server
    with stream:
        while True:
            try:
                indata = await input_queue.get()
                await ws.send(indata)
            except asyncio.CancelledError:
                break

async def send_text(ws):
    """Send text messages to WebSocket server."""
    loop = asyncio.get_event_loop()
    while True:
        try:
            text = await loop.run_in_executor(None, input, "> ")
            await ws.send(text)
            if text.lower() == "exit":
                # Send 'submit_response' to signal end of audio stream
                await ws.send("submit_response")
                break
        except asyncio.CancelledError:
            break

async def receive_transcriptions(ws):
    """Receive transcriptions from WebSocket server."""
    try:
        async for message in ws:
            print(f"Received: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed.")

async def test_websocket():
    uri = "ws://localhost:8000/TranscribeStreaming"
    async with websockets.connect(uri) as ws:

        send_audio_task = asyncio.create_task(send_audio(ws))
        receive_task = asyncio.create_task(receive_transcriptions(ws))
        send_text_task = asyncio.create_task(send_text(ws))

        await send_text_task  # Wait until user types 'exit' to end

        # Cancel other tasks
        send_audio_task.cancel()
        receive_task.cancel()

        await asyncio.gather(send_audio_task, receive_task, return_exceptions=True)

        # Close the websocket connection after processing
        await ws.close()

if __name__ == "__main__":
    asyncio.run(test_websocket())