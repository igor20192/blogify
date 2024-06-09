# Blogify

Blogify is a web application based on Django that allows you to publish and 
view articles. Telegram bot for notifications is also integrated into the project
new articles and a script for scrapping news from Hacker News.

## Installation

### Using Docker

1. Clone the repository:

    ```sh
    git clone https://github.com/igor20192/blogify.git
    cd blogify
    ```

2. Create a file `.env` for environment variables:

    ```env
    DEBUG=1
    SECRET_KEY=your-secret-key
    TELEGRAM_TOKEN=your-telegram-bot-token
    ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    DATABASE_URL=postgres://postgres:password@db:5432/postgres
    ```

3. Create a file `.env.db` for the database:

    ```env
    POSTGRES_DB=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password
    ```

4. Start Docker Containers:

    ```sh
    docker-compose up --build
    ```

5. Open your browser and go to the ː`http://localhost:8080` address to access 
   annex.

### Local installation (without Docker)

1. Clone the repository:

    ```sh
    git clone https://github.com/igor20192/blogify.git
    cd blogify
    ```

2. Create a virtual environment and activate it:

    ```sh
    python3 -m venv blogify_env
    source blogify_env/bin/activate
    ```

3. Set the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Perform database migration:

    ```sh
    python manage.py migrate
    ```

5. Create a root to access the panel admin:

    ```sh
    python manage.py createsuperuser
    ```

6. Start the development server:

    ```sh
    python manage.py runserver
    ```

## Telegram Bot

Telegram bot is used to receive notifications about new articles and execution 
teams. 

### Команды бота

- `/start` — welcome note.
- `/help` — list of available commands and their descriptions.
- `/latest` — get latest article.
- `/subscribe` — subscribe to notifications about new articles.

### Bot setting

1. Get a bot token from [BotFather](https://t.me/botfather) in Telegram.
2. Add a token to the Django settings (`settings.py`):

    ```python
    TELEGRAM_TOKEN = 'your-telegram-bot-token'
    ```

3. Start the bot script:

    ```sh
    python telegram_bot.py
    ```

## Script for scrapping news

Script for scraping news from the site Hacker News collects headers and URLs 
news articles and stores them in a database.

### Used library

- `requests`
- `BeautifulSoup`
- `logging`

### Script run

1. Ensure that the virtual environment is activated.
2. Run the script:

    ```sh
    python news/news_scraper.py
    ```

### Planning a Script Run with cron

1. Open crontab for editing:

    ```sh
    crontab -e
    ```

2. Add a task to run the script (for example, every hour):

    ```sh
    0 * * * * /path/to/blogify_env/bin/python /path/to/blogify/news/news_scraper.py
    ```

## Docker configuration

### `docker-compose.yml`

```yaml
version: '3'

services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env.db
    ports:
      - 5432:5432
  web:
    build: .
    command: >
      bash -c "python manage.py makemigrations &&
        python manage.py migrate &&
        python manage.py runserver 0.0.0.0:8080"
    restart: always
    volumes:
      - ./media/:/usr/src/blogify/media/
    ports:
      - 8080:8080
    env_file:
      - ./.env
    depends_on:
      - db

volumes:
  postgres_data:
```
### `Dockerfile`
# pull official base image
FROM python:3.12-bullseye

# set work directory
WORKDIR /usr/src/blogify

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

# install dependencies
RUN apt-get update && \
    apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    gettext && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y \
    gcc \
    pkg-config && \
    rm -rf /var/lib/apt/lists/*

# copy project
COPY . .

# Blogify Project

Blogify is a Django-based web application for managing and displaying articles. It includes a news scraping feature and a Telegram bot for notifications.

## Project Structure

```plaintext
blogify/
├── blogify_env/         # virtual environment
├── blog/                # Django application for managing articles
│   ├── migrations/      # Database migration
│   ├── static/          # static files
│   ├── templates/       # Django templates
│   ├── admin.py         # Panel admin configuration
│   ├── apps.py          # Application configuration
│   ├── models.py        # Data model
│   ├── views.py         # Views (Views)
│   ├── urls.py          # Routing
│   └── signals.py       # Signals
├── news/                # App for scrapping news
│   ├── migrations/      # Database migration
│   ├── static/          # Static files
│   ├── templates/       # Django templates
│   ├── admin.py         # Panel admin configuration
│   ├── apps.py          # Application configuration
│   ├── models.py        # Data model
│   ├── views.py         # Views (Views)
│   ├── urls.py          # Routing
│   └── news_scraper.py  # Script for scrapping news
├── blogify/             # Django project configuration
│   ├── __init__.py
│   ├── settings.py      # Django settings
│   ├── urls.py          # Project routing
│   └── wsgi.py          # WSGI settings for deployment
├── manage.py            # Django project management master script
├── requirements.txt     # Project dependencies
└── telegram_bot.py      # Telegram bot script
```

### Licence

This project is licensed under the MIT licence. See the LICENSE file for details.
