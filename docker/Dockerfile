# Use official Python image
FROM python:3.12-slim

# Build arguments for versioning
ARG APP_VERSION=latest
ARG BUILD_DATE=unknown
ARG GIT_COMMIT=unknown

# Labels for image metadata
LABEL org.opencontainers.image.version="$APP_VERSION"
LABEL org.opencontainers.image.created="$BUILD_DATE"
LABEL org.opencontainers.image.revision="$GIT_COMMIT"
LABEL org.opencontainers.image.title="Telegram Reposting Bot"
LABEL org.opencontainers.image.description="AI-powered Telegram bot for reposting content"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ../requirements/ /requirements

# Install Python dependencies
RUN pip install --no-cache-dir -r /requirements/prod-requirements.txt
RUN pip install --no-cache-dir -r /requirements/dev-requirements.txt

# Copy bot source code
COPY ../src /app/src
COPY ../main.py /app/main.py

# Set environment variables (can be overridden by docker-compose)
ENV PYTHONUNBUFFERED=1
ENV APP_VERSION=$APP_VERSION
ENV BUILD_DATE=$BUILD_DATE
ENV GIT_COMMIT=$GIT_COMMIT

# Start the bot
CMD ["python", "/app/main.py"]
