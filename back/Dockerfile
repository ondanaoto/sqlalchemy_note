FROM python:3.12-slim

# psycopg2 をビルドできるようライブラリを追加
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml .

RUN uv sync