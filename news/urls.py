from django.urls import path
from .views import NewsArticleListCreate

urlpatterns = [
    path("news/", NewsArticleListCreate.as_view(), name="news-article-list-create"),
]
