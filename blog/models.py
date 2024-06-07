from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    """The Article model represents a blog article.

    Attributes:
    - title: The title of the article.
    - content: The content of the article.
    - published_date: The date and time the article was published.
    - author: The author of the article. Reference to User model.

    Methods:
    - __str__: Returns a string representation of the Article object."""

    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Subscriber(models.Model):
    chat_id = models.CharField(max_length=100)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.chat_id
