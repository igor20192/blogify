import logging
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article, Subscriber
from .serializers import ArticleSerializer, SubscriberSerializer
from .permissions import IsAuthorOrAdmin
from decouple import config


class ArticleListCreate(generics.ListCreateAPIView):
    """A view class for viewing a list of articles and creating a new article.

    Attributes:
    - queryset: A dataset containing all Article objects.
    - serializer_class: Serializer class used for validation and serialisation of data.
    - permission_classes: Permission classes used to validate user permissions."""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """A method to save the author when creating a new article.

        Parameters:
        - serializer: Serialiser for data validation.
        """
        serializer.save(author=self.request.user)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    """A view class for viewing, updating, and deleting a specific article.

    Attributes:
    - queryset: A dataset containing all Article objects.
    - serializer_class: A serialiser class used for validating and serialising data.
    - permission_classes: Permission classes used to validate user permissions."""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """A method to define permission classes depending on the HTTP method.

        Returns:
        - A list of permission classes."""
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAuthenticated(), IsAuthorOrAdmin()]


class LatestArticleView(APIView):
    """
    API endpoint that retrieves and returns the latest published article.

    This view class provides a GET method that fetches the most recently published
    article from the database using the `Article.objects.latest` queryset method.
    It then serializes the article data using the `ArticleSerializer` and returns
    a JSON response containing the serialized data.

    This endpoint is useful for clients (e.g., mobile apps, web applications) that
    need to display the latest article information.

    Raises:
        DoesNotExist: If no articles exist in the database."""

    def get(self, request, format=None):
        latest_article = Article.objects.latest("published_date")
        serializer = ArticleSerializer(latest_article)
        return Response(serializer.data)


class SubscriberApiView(APIView):
    """
    API view to handle subscriber creation.

    This view handles the POST request to create a subscriber. It requires
    `chat_id`, `username`, and `password` to be provided in the request data.
    If the provided username and password match the expected values from the
    environment variables, a new subscriber is created if it doesn't already exist.

    Methods:
        post(request, *args, **kwargs): Handles the POST request to create a subscriber.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to create a new subscriber.

        Args:
            request (Request): The HTTP request object containing subscriber data.

        Returns:
            Response: The HTTP response object containing a success or error message.
        """

        chat_id = request.data.get("chat_id")
        username = request.data.get("username")
        password = request.data.get("password")
        if not chat_id or not username or not password:
            return Response(
                {"message": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if username == config("TELEGRAM_USER") and password == config(
            "TELEGRAM_PASSWORD"
        ):
            subscriber, created = Subscriber.objects.get_or_create(chat_id=chat_id)
            if created:
                return Response(
                    {"message": "Subscription created successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"message": "Already subscribed."}, status=status.HTTP_200_OK
                )
        return Response(
            {"message": "Incorrect login or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
