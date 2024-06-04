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