import asyncio
import websockets

async def receive_and_respond(ws):
    try:
        async for message in ws:
            print(f"Received from server: {message}")
            # Process the message and prepare a response
            response = f"Response to: {message}"
            await ws.send(response)
            print(f"Sent to server: {response}")
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket connection closed.")

async def main():
    uri = "ws://localhost:8000/TranscribeStreaming"
    async with websockets.connect(uri) as ws:
        receive_task = asyncio.create_task(receive_and_respond(ws))

        # Keep the connection open
        await receive_task

if __name__ == "__main__":
    asyncio.run(main())