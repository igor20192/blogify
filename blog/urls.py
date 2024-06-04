from django.urls import path
from .views import ArticleListCreate, ArticleDetail

urlpatterns = [
    path("articles/", ArticleListCreate.as_view(), name="article-list-create"),
    path("articles/<int:pk>/", ArticleDetail.as_view(), name="article-detail"),
]
