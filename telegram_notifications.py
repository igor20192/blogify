import logging
from asgiref.sync import sync_to_async
from blog.models import Subscriber
from django.conf import settings
from telegram import Bot

logging.basicConfig(
    filename="telegram_bot.log",
    format="[%(asctime)s] [%(levelname)s] => %(message)s]",
    level=logging.INFO,
)


async def notify_subscribers(article):
    """
    Asynchronously notifies subscribers about a new blog article.

    This function retrieves all subscribers from the `Subscriber` model,
    creates a Telegram bot instance using the `TELEGRAM_TOKEN` from Django settings,
    and sends a message to each subscriber's chat ID with details about the new article.

    Args:
        article (object): The new blog article object to be notified about.
            Its attributes (`title` and `content`) are expected to be strings.

    Raises:
        Exception: Any exception that occurs during the notification process.
            The exception details are logged to the `telegram_bot.log` file.
    """
    try:
        subscribers = await sync_to_async(list)(Subscriber.objects.all())
        bot = Bot(token=settings.TELEGRAM_TOKEN)
        for subscriber in subscribers:
            await bot.send_message(
                chat_id=subscriber.chat_id,
                text=f"Новая статья:\n\n{article.title}\n\n{article.content}",
            )
    except Exception as e:
        logging.exception(f"Error in notify_subscribers: {e}")
