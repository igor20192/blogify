from re import T
from django import dispatch
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article
import asyncio
from telegram_notifications import notify_subscribers


@receiver(post_save, sender=Article)
def article_post_save(sender, instance, created, **kwargs):
    """
    Asynchronous signal handler for Article model post-save events.

    This function is registered as a receiver for the `post_save` signal emitted by
    the `Article` model. It is designed to handle new article creation specifically.

    When a new article is saved (indicated by `created=True`), it performs the following actions:
        1. Checks if the article has a primary key (`pk`) and hasn't been notified yet (`notified=False`).
        2. If both conditions are met, sets `notified` to `True` to prevent duplicate notifications.
        3. Saves the updated article instance with `update_fields=["notified"]`.
        4. Asynchronously executes the `notify_subscribers` function (assumed to be imported)
           to notify subscribers about the new article using a Telegram bot (implementation details
           depend on `telegram_notifications`).

    Args:
        sender (Model): The model class that sent the signal (in this case, `Article`).
        instance (Article): The specific article instance that was saved.
        created (bool): Indicates whether a new object was created (`True`) or an existing one
                        was updated (`False`).
        **kwargs: Additional keyword arguments passed by the signal.
    """
    if created and instance.pk and not instance.notified:
        instance.notified = True
        instance.save(update_fields=["notified"])
        asyncio.run(notify_subscribers(instance))
