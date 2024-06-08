import os
import sys
import django
import logging
import requests
from bs4 import BeautifulSoup
from django.conf import settings


# Define the path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Add project root to system path
sys.path.append(project_root)
# Set the environment variable for the Django configuration file
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogify.settings")
django.setup()

# Import model after configuring Django
from news.models import NewsArticle

# Configure logging
logging.basicConfig(
    filename="news_scraper.log",
    format="[%(asctime)s] [%(levelname)s] => %(message)s]",
    level=logging.INFO,
)


def fetch_news():
    """
    Fetches news articles from Hacker News (https://news.ycombinator.com/).

    This function scrapes the Hacker News homepage and retrieves titles and URLs
    of the listed articles. It returns a list of dictionaries, where each dictionary
    contains a 'title' and a 'url' key.

    Returns:
        list[dict]: A list of dictionaries containing news article information
                    (title and URL), or an empty list if no articles are found.
    """
    url = "https://news.ycombinator.com/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Checking for HTTP errors
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


def save_news(news_items: list[dict]) -> None:
    """
    Saves fetched news articles to the database.

    This function iterates through the provided list of news articles (dictionaries)
    and attempts to create them in the `NewsArticle` model. If an article with the
    same title and URL already exists, it is skipped to avoid duplicates. Any exceptions
    encountered during saving are logged for debugging purposes.

    Args:
        news_items (list[dict]): A list of dictionaries containing news article information
                                (title and URL).
    """
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
