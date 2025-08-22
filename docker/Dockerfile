# Use official Python image
FROM python:3.12-slim

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

# Start the bot
CMD ["python", "/app/main.py"]
