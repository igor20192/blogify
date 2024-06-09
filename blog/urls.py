from django.urls import path
from .views import (
    ArticleListCreate,
    ArticleDetail,
    LatestArticleView,
    SubscriberApiView,
)

urlpatterns = [
    path("articles/", ArticleListCreate.as_view(), name="article-list-create"),
    path("articles/<int:pk>/", ArticleDetail.as_view(), name="article-detail"),
    path("articles/latest/", LatestArticleView.as_view(), name="latest-article"),
    path("subscribe/", SubscriberApiView.as_view(), name="subscribe"),
]
