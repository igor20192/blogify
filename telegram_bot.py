import json
import os
import logging
import aiohttp
import django
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from asgiref.sync import sync_to_async
from decouple import config

logging.basicConfig(
    filename="telegram_bot.log",
    format="[%(asctime)s] [%(levelname)s] => %(message)s]",
    level=logging.INFO,
)


# Create an Application Object
application = Application.builder().token(config("TELEGRAM_TOKEN")).build()


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
            "Available commands:\n/start - Welcome message\n/help - List of commands\n/latest - Get the latest article.\n/subscribe - Subscribe to blog updates."
        )
    except Exception as e:
        logging.exception(f"Error in help command: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")


async def get_latest_article():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{config('API_URL')}/api/articles/latest/"
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
            message = f"Recent article:\n\n{response['title']}\n\n{response['content']}"
        else:
            message = "Couldn’t get a fresh article."

        await update.message.reply_text(message)
    except Exception as e:
        logging.error(f"Error in latest command: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        chat_id = update.message.chat_id
        data = {
            "chat_id": chat_id,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{config('API_URL')}/api/subscribe/", json=data
            ) as response:

                if response.status == 201:
                    message = "You have successfully subscribed to the blog updates."
                else:
                    message = "You have already subscribed to the blog updates."
                await update.message.reply_text(message)
    except Exception as e:
        logging.error(f"Error in subscribe command: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")


def main():
    try:
        # add software handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("latest", latest))
        application.add_handler(CommandHandler("subscribe", subscribe))

        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logging.error(f"Error in main function: {e}")


if __name__ == "__main__":
    main()
