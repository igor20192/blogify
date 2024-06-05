import os
import logging
from urllib import response
import aiohttp
import asyncio
import django
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from asgiref.sync import sync_to_async

logging.basicConfig(
    filename="telegram_bot.log", format="[%(asctime)s] [%(levelname)s] => %(message)s]"
)

# Установите переменную окружения для файла настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogify.settings")

# Инициализируйте Django
django.setup()

# Теперь вы можете импортировать модели и доступ к настройкам
from blog.models import Article  # Импортируйте ваши модели
from django.conf import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Use /latest to get the latest article.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Available commands:\n/start - Welcome message\n/help - List of commands\n/latest - Get the latest article."
    )


async def get_latest_article():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.API_URL}/api/articles/latest1/") as response:
            assert response.status == 200
            return await response.json()


async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    response = await get_latest_article()
    if response:

        message = f"Recent article:\n\n{response['title']}\n\n{response['content']}"

    else:
        message = "Не удалось получить свежую статью."
    await update.message.reply_text(message)


def main():
    # Создаем объект приложения
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("latest", latest))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":

    main()
