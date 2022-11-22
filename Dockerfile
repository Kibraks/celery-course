FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY pyproject.toml poetry.lock /app/


RUN apt-get update && \
    apt-get install -y \
        gcc \
        build-essential \
        libpq-dev \
        python3-dev \
        procps \
        telnet && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry install --no-root

COPY . .

RUN chmod +x /app/scripts
