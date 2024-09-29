import telebot
import requests

# Telegram Bot setup
bot = telebot.TeleBot("7238562180:AAGt88x25LzLTBnoxzVEj8kGmGWXybzxyZg")
bot.remove_webhook()

# Webhook URL
WEBHOOK_URL = 'http://localhost:5002/webhooks/rest/webhook'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['help'])
def reply_chat(message):
    # Echo back to Telegram
    bot.reply_to(message, f"You said: {message.text}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Send message via webhook
    send_message_via_webhook(message, message.text)
    
    # Echo back to Telegram
    bot.reply_to(message, f"You said: {message.text}")

def send_message_via_webhook(message, text):
    print("Sending message now...")
    r = requests.post(WEBHOOK_URL, json={"sender": "jack", "message": text})
    print("Webhook response:")
    for i in r.json():
        bot.reply_to(message, f"You said: {i}")

# Start polling
bot.infinity_polling()