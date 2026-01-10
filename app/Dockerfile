# --- Stage 1: Builder ---
FROM python:3.12-slim AS builder

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /install

# Install system dependencies required for building lxml and other Scrapy deps
RUN apt-get update && apt-get install -y \
    gcc \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies to a temporary location
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# --- Stage 2: Runtime ---
FROM python:3.12-slim

WORKDIR /app

# Copy the installed python packages from the builder stage
COPY --from=builder /install /usr/local

# Copy the project files
COPY . .

# Ensure the app creates a placeholder for the hourly news output
RUN touch /app/hourly_news.jsonl && chmod 666 /app/hourly_news.jsonl

# Security: Run as a non-privileged user
RUN useradd -m scraper
USER scraper

# Set the entrypoint to the scrapy command
ENTRYPOINT ["scrapy"]

# Default command if none is provided
CMD ["crawl", "articles"]
