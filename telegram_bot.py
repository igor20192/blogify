import os
import logging
import aiohttp
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
from blog.models import Subscription  # Импортируйте ваши модели
from django.conf import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text(
            "Welcome! Use /latest to get the latest article."
        )
    except Exception as e:
        logging.exception(f"Error in start command: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text(
            "Available commands:\n/start - Welcome message\n/help - List of commands\n/latest - Get the latest article.\n/subscribe - "
        )
    except Exception as e:
        logging.exception(f"Error in help command: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")


async def get_latest_article():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{settings.API_URL}/api/articles/latest/"
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logging.error(f"Failed to fetch latest article: {response.status}")
                    return None
    except Exception as e:
        logging.exception(f"Error in get_latest_article: {e}")
        return None


async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = await get_latest_article()
        if response:
            message = f"Fresh article:\n\n{response['title']}\n\n{response['content']}"
        else:
            message = "It was not possible to get a recent article."
        await update.message.reply_text(message)
    except Exception as e:
        logging.exception(f"Error in latest command: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = await update.message.chat_id
    user = await update.message.from_user
    sync_to_async(Subscription.objects.get_or_create(user=user, chat_id=chat_id))
    await update.message.reply_text("Вы подписаны на обновления блога.")


def main():
    try:
        # Создаем объект приложения
        application = Application.builder().token(settings.TELEGRAM_TOKEN).build()

        # Добавляем обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("latest", latest))
        application.add_handler(CommandHandler("subscribe", subscribe))

        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logging.exception(f"Error in main function: {e}")


if __name__ == "__main__":
    main()
