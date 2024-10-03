import asyncio
import websockets
import aiohttp
import threading
import telebot
import logging
import janus  # Import janus for thread-safe queues

# Configure logging
logging.basicConfig(level=logging.INFO)

# Telegram Bot setup
bot_token = "7238562180:AAGt88x25LzLTBnoxzVEj8kGmGWXybzxyZg"  # Replace with your Telegram bot token
bot = telebot.TeleBot(bot_token)
bot.remove_webhook()

# Set TeleBot logging level to WARNING to suppress unnecessary error messages
telebot_logger = logging.getLogger('telebot')
telebot_logger.setLevel(logging.WARNING)

async def send_to_rasa(message, sender_id):
    try:
        async with aiohttp.ClientSession() as session:
            rasa_url = 'http://localhost:5002/webhooks/rest/webhook'
            payload = {"sender": sender_id, "message": message}
            async with session.post(rasa_url, json=payload) as resp:
                if resp.status == 200:
                    response = await resp.json()
                    return response
                else:
                    logging.error(f"Received non-200 response from Rasa: {resp.status}")
                    return []
    except Exception as e:
        logging.error(f"Error communicating with Rasa: {e}")
        return []

async def process_messages(message_queue):
    while True:
        source, sender, message = await message_queue.async_q.get()
        logging.info(f"Processing message from {source}: {message}")
        sender_id = str(sender)
        # Send message to Rasa AI
        rasa_response = await send_to_rasa(message, sender_id)
        if rasa_response:
            for resp in rasa_response:
                reply_text = resp.get('text')
                if reply_text:
                    if source == "telebot":
                        bot.send_message(sender, reply_text)
                    elif source == "robot":
                        try:
                            await sender.send(reply_text)
                        except Exception as e:
                            logging.error(f"Error sending message to robot: {e}")
        else:
            # Handle case where Rasa response is empty or failed
            error_message = "Sorry, I couldn't process your request."
            if source == "telebot":
                bot.send_message(sender, error_message)
            elif source == "robot":
                try:
                    await sender.send(error_message)
                except Exception as e:
                    logging.error(f"Error sending error message to robot: {e}")

def start_telebot(message_queue):
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, "Hello! How can I assist you today?")

    # Handler for text messages
    @bot.message_handler(content_types=['text'])
    def handle_text_message(message):
        # Put the message text into the queue
        message_queue.sync_q.put(("telebot", message.chat.id, message.text))
        # Optionally, acknowledge receipt
        # bot.reply_to(message, f"Received your message: {message.text}")

    # Handler for photos
    @bot.message_handler(content_types=['photo'])
    def handle_photo_message(message):
        bot.reply_to(message, "Sorry, I can't handle images.")

    # Handler for audio
    @bot.message_handler(content_types=['audio'])
    def handle_audio_message(message):
        bot.reply_to(message, "Sorry, I can't handle audio files.")

    # Handler for video
    @bot.message_handler(content_types=['video'])
    def handle_video_message(message):
        bot.reply_to(message, "Sorry, I can't handle video files.")

    # Handler for other content types (documents, stickers, etc.)
    @bot.message_handler(content_types=['document', 'sticker', 'voice', 'video_note', 'location', 'contact'])
    def handle_other_message(message):
        bot.reply_to(message, "Sorry, I can't handle this type of information.")

    # Start polling
    bot.infinity_polling(timeout=4, long_polling_timeout=4)
    
async def handle_robot_messages(websocket, path, message_queue):
    try:
        async for message in websocket:
            logging.info(f"Received from robot: {message}")
            # Put the message into the queue
            await message_queue.async_q.put(("robot", websocket, message))
    except websockets.exceptions.ConnectionClosed:
        logging.info("WebSocket connection closed with robot.")

async def main():
    # Initialize the message queue
    message_queue = janus.Queue()

    # Start the message processing task
    asyncio.create_task(process_messages(message_queue))

    # Start the Telebot in a separate thread
    telebot_thread = threading.Thread(target=start_telebot, args=(message_queue,), daemon=True)
    telebot_thread.start()

    # Start the websocket server for robot messages
    server = await websockets.serve(
        lambda ws, path: handle_robot_messages(ws, path, message_queue),
        "0.0.0.0", 8001
    )
    logging.info("Assistant is listening on ws://localhost:8001")

    # Keep the main function running
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
