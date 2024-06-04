from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Article


class ArticleTests(APITestCase):

    def setUp(self):
        # Set up two users
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")

        # Set up a client
        self.client = APIClient()

        # Create an article by user1
        self.article = Article.objects.create(
            title="Test Article", content="Content of test article", author=self.user1
        )

    def test_create_article_authenticated(self):
        # Log in as user1
        self.client.login(username="user1", password="password123")

        # Define the data for the new article
        data = {"title": "New Article", "content": "New content"}

        # Make a POST request to create a new article
        response = self.client.post("/api/articles/", data, format="json")

        # Check if the response status is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the article is created with the correct author
        self.assertEqual(response.data["author"], self.user1.id)

    def test_create_article_unauthenticated(self):
        # Define the data for the new article
        data = {"title": "New Article", "content": "New content"}

        # Make a POST request to create a new article without authentication
        response = self.client.post("/api/articles/", data, format="json")

        # Check if the response status is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_article(self):
        # Log in as user2
        self.client.login(username="user2", password="password123")

        # Make a GET request to retrieve the article
        response = self.client.get(f"/api/articles/{self.article.id}/")

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the returned article is the one we created
        self.assertEqual(response.data["id"], self.article.id)

    def test_update_article_by_author(self):
        # Log in as user1 (author of the article)
        self.client.login(username="user1", password="password123")

        # Define the data for updating the article
        data = {"title": "Updated Article", "content": "Updated content"}

        # Make a PUT request to update the article
        response = self.client.put(
            f"/api/articles/{self.article.id}/", data, format="json"
        )

        # Check if the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the article is updated
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, "Updated Article")
        self.assertEqual(self.article.content, "Updated content")

    def test_update_article_by_non_author(self):
        # Log in as user2 (not the author of the article)
        self.client.login(username="user2", password="password123")

        # Define the data for updating the article
        data = {"title": "Updated Article", "content": "Updated content"}

        # Make a PUT request to update the article
        response = self.client.put(
            f"/api/articles/{self.article.id}/", data, format="json"
        )

        # Check if the response status is 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_article_by_author(self):
        # Log in as user1 (author of the article)
        self.client.login(username="user1", password="password123")

        # Make a DELETE request to delete the article
        response = self.client.delete(f"/api/articles/{self.article.id}/")

        # Check if the response status is 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if the article is deleted
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())

    def test_delete_article_by_non_author(self):
        # Log in as user2 (not the author of the article)
        self.client.login(username="user2", password="password123")

        # Make a DELETE request to delete the article
        response = self.client.delete(f"/api/articles/{self.article.id}/")

        # Check if the response status is 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
