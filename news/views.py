from django.shortcuts import render
from rest_framework import generics
from .models import NewsArticle
from .serializers import NewsArticleSerializer


class NewsArticleListCreate(generics.ListCreateAPIView):
    """
    API view to retrieve list of news articles or create new ones.

    This view handles two types of requests:

    1. GET: Returns a list of all news articles in the database.
    2. POST: Allows the creation of new news articles. The request body should contain
       the necessary data fields as defined in the `NewsArticleSerializer`.

    Attributes:
        queryset (QuerySet): The queryset that provides the list of news articles.
        serializer_class (Serializer): The serializer class used to validate and serialize data.

    Methods:
        get_queryset(): Returns the queryset of all news articles.
        get_serializer_class(): Returns the serializer class for the news articles.
    """

    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
