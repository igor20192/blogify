import os
import logging
import pdb
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from django.conf import settings
import django
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogify.settings")

django.setup()


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define the bot commands
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Привет! Я ваш блог-бот. Используйте команду /help для получения списка доступных команд."
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Список доступных команд:\n"
        "/start - приветственное сообщение.\n"
        "/help - список доступных команд и их описания.\n"
        "/latest - получить свежую статью из блога."
    )


def latest(update: Update, context: CallbackContext) -> None:
    response = requests.get(f"{settings.API_URL}/api/articles/latest/")
    if response.status_code == 200:
        article = response.json()
        message = f"Свежая статья:\n\n{article['title']}\n\n{article['content']}"
    else:
        message = "Не удалось получить свежую статью."
    update.message.reply_text(message)


def main() -> None:
    # Initialize bot and updater
    updater = Updater(bot=Bot, update_queue=settings.TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("latest", latest))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
