
import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import CallbackContext
from telegram.error import TelegramError, NetworkError

import asyncio

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("webhook_bot")

# Инициализация
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Обработчики
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await bot.send_message(chat_id=chat_id, text="Привет! Я читаю QR-коды. Отправь мне изображение.")

async def help_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await bot.send_message(chat_id=chat_id, text="Просто отправь мне изображение с QR-кодом.")

async def handle_image(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    await bot.send_message(chat_id=chat_id, text="Изображение получено! (обработка не реализована)")

@app.route("/webhook/telegram", methods=["POST"])
async def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)

    if update.message:
        message = update.message
        context = CallbackContext.from_update(update, bot)

        if message.text == "/start":
            await start(update, context)
        elif message.text == "/help":
            await help_command(update, context)
        elif message.photo:
            await handle_image(update, context)

    return "ok", 200

@app.route("/status", methods=["GET"])
def status():
    if TOKEN:
        return "Railway QR Bot работает!"
    return "Токен не найден", 500

@app.route("/setup-webhook", methods=["GET"])
async def setup_webhook():
    url = "https://qrr2-go.up.railway.app/webhook/telegram"
    try:
        await bot.set_webhook(url)
        return f"✅ Webhook успешно установлен на {url}"
    except (TelegramError, NetworkError, Exception) as e:
        logger.error("Ошибка при установке webhook: %s", str(e))
        return f"❌ Ошибка установки webhook: {str(e)}", 500
