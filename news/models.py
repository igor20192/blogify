from django.db import models
from django.db import models


class NewsArticle(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
