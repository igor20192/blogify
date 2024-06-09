from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article, Subscriber
from .serializers import ArticleSerializer, SubscriberSerializer
from .permissions import IsAuthorOrAdmin


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
    API view to handle subscription requests.

    This view processes POST requests to create a new subscription based on the provided
    chat ID. If the chat ID is already subscribed, it returns a message indicating that
    the user is already subscribed. Otherwise, it creates a new subscription and returns
    a success message.

    Attributes:
        permission_classes (list): List of permission classes that determine access to the view.

    Methods:
        post(request, *args, **kwargs): Handles POST requests to create a new subscription.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new subscription.

        Args:
            request (Request): The HTTP request object containing data for creating a new subscription.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response object containing a message and an appropriate HTTP status code.
                - If the subscription is created successfully, returns a 201 Created status.
                - If the chat ID is already subscribed, returns a 200 OK status.
        """
        chat_id = request.data.get("chat_id")
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
