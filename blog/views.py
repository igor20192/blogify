from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer
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
