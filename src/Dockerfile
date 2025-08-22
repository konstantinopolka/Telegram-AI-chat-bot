# Use official Python image
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ../requirements/prod-requirements.txt ./requirements.txt
COPY ../requirements/base-requirements.txt ./base-requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot source code
COPY . .

# Set environment variables (can be overridden by docker-compose)
ENV PYTHONUNBUFFERED=1

# Start the bot
CMD ["python", "/app/main.py"]
