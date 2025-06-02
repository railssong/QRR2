
import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, filters
from telegram.ext import CallbackContext

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("webhook_bot")

# Инициализация
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Обработчики
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text="Привет! Я читаю QR-коды. Отправь мне изображение.")

def help_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text="Просто отправь мне изображение с QR-кодом.")

def handle_image(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text="Изображение получено! (обработка не реализована)")

# Webhook
@app.route("/webhook/telegram", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    if update.message:
        message = update.message
        context = CallbackContext.from_update(update, bot)

        if message.text == "/start":
            start(update, context)
        elif message.text == "/help":
            help_command(update, context)
        elif message.photo:
            handle_image(update, context)

    return "ok", 200

# Служебные маршруты
@app.route("/status", methods=["GET"])
def status():
    return "Railway QR Bot работает!"

@app.route("/setup-webhook", methods=["GET"])
def setup_webhook():
    url = f"{request.url_root}webhook/telegram"
    bot.set_webhook(url)
    return f"Webhook успешно установлен на {url}"
