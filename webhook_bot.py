
import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder, ContextTypes, Dispatcher
from PIL import Image
import io
import logging

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
app = Flask(__name__)

# Логгирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("webhook_bot")

# Сюда мы сохраним диспетчер (Dispatcher) для обработки сообщений
dispatcher: Dispatcher = Dispatcher(bot=bot, update_queue=None, workers=1, use_context=True)

def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text("Привет! Я читаю QR-коды. Отправь мне изображение.")

def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text("Просто отправь мне изображение с QR-кодом.")

def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text("Изображение получено! (Обработка QR-кода не реализована)")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(MessageHandler(filters.PHOTO, handle_image))

@app.route("/webhook/telegram", methods=["POST"])
def telegram_webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return "ok", 200

@app.route("/status", methods=["GET"])
def status():
    return "Railway QR Bot работает!"

@app.route("/setup-webhook", methods=["GET"])
def setup_webhook():
    url = f"{request.url_root}webhook/telegram"
    bot.set_webhook(url)
    return f"Webhook успешно установлен на {url}"
