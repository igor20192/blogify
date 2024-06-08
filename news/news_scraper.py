import os
import sys
import django
import logging
import requests
from bs4 import BeautifulSoup
from django.conf import settings

# Добавьте корневую директорию проекта в путь поиска Python
# sys.path.append("/home/igor/Projects/blogify")

# Определите путь к корню проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Добавьте корень проекта в системный путь
sys.path.append(project_root)
# Установите переменную окружения для файла настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogify.settings")
django.setup()

# Импортируйте модель после настройки Django
from news.models import NewsArticle

# Настройка логирования
logging.basicConfig(
    filename="news_scraper.log",
    format="[%(asctime)s] [%(levelname)s] => %(message)s]",
    level=logging.INFO,
)


def fetch_news():
    url = "https://news.ycombinator.com/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на HTTP ошибки
    except requests.RequestException as e:
        logging.error(f"Error fetching the page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    news_items = []

    for item in soup.select(".titleline"):
        title = item.get_text()
        url = item.a.get("href")
        news_items.append({"title": title, "url": url})

    return news_items


def save_news(news_items):
    for item in news_items:
        try:
            NewsArticle.objects.get_or_create(title=item["title"], url=item["url"])
        except Exception as e:
            logging.error(f"Error saving article {item['title']}: {e}")


if __name__ == "__main__":
    news_items = fetch_news()
    if news_items:
        save_news(news_items)
        logging.info("News articles fetched and saved successfully.")
    else:
        logging.info("No news articles fetched.")
