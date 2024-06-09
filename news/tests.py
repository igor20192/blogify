from django.test import TestCase
import json
from django.test import TestCase, Client
from django.urls import reverse
from news.models import NewsArticle


class NewsArticleTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_url = reverse("news-article-list-create")
        self.article1 = NewsArticle.objects.create(
            title="Article 1", url="http://example.com/1"
        )
        self.article2 = NewsArticle.objects.create(
            title="Article 2", url="http://example.com/2"
        )

    def test_get_news_articles(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data.get("count"), 2)
        self.assertEqual(data.get("results")[0]["title"], self.article1.title)
        self.assertEqual(data.get("results")[0]["url"], self.article1.url)
        self.assertEqual(data.get("results")[1]["title"], self.article2.title)
        self.assertEqual(data.get("results")[1]["url"], self.article2.url)

    def test_create_news_article(self):
        data = {"title": "New Article", "url": "http://example.com/new"}

        response = self.client.post(
            self.list_url, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

        response_data = response.json()
        self.assertEqual(response_data["title"], data["title"])
        self.assertEqual(response_data["url"], data["url"])

        articles = NewsArticle.objects.all()
        self.assertEqual(articles.count(), 3)
        new_article = NewsArticle.objects.get(title="New Article")
        self.assertEqual(new_article.url, data["url"])
