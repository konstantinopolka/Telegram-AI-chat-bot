#!/bin/bash

# Telegram Bot Startup Script
# This script starts the FastAPI server, exposes it via ngrok, and sets up the webhook

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PORT=${PORT:-8000}  # Default to 8000 if PORT not set

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    printf "${YELLOW}Activating virtual environment...${NC}\n"
    source venv/bin/activate
else
    printf "${YELLOW}No virtual environment found. Creating one...${NC}\n"
    python3 -m venv venv
    source venv/bin/activate
    printf "${YELLOW}Installing dependencies...${NC}\n"
    pip install -r requirements.txt
fi

# Check if uvicorn is available
if ! command -v uvicorn &> /dev/null; then
    printf "${YELLOW}Installing uvicorn...${NC}\n"
    pip install uvicorn
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    printf "${RED}Error: .env file not found!${NC}\n"
    printf "Please create a .env file with your TELEGRAM_TOKEN\n"
    exit 1
fi

# Load environment variables
source .env

# Check if TELEGRAM_TOKEN is set
if [ -z "$TELEGRAM_TOKEN" ]; then
    printf "${RED}Error: TELEGRAM_TOKEN not found in .env file!${NC}\n"
    exit 1
fi

# Kill any existing ngrok processes to avoid session limit
printf "${YELLOW}Checking for existing ngrok processes...${NC}\n"
pkill -f ngrok 2>/dev/null || true
sleep 2

printf "${GREEN}Starting Telegram Bot...${NC}\n"

# Function to cleanup background processes
cleanup() {
    printf "\n${YELLOW}Shutting down...${NC}\n"
    if [ ! -z "$UVICORN_PID" ]; then
        kill $UVICORN_PID 2>/dev/null
        printf "Stopped FastAPI server\n"
    fi
    if [ ! -z "$NGROK_PID" ]; then
        kill $NGROK_PID 2>/dev/null
        printf "Stopped ngrok tunnel\n"
    fi
    exit 0
}

# Set up trap to cleanup on script exit
trap cleanup SIGINT SIGTERM EXIT

# 1. Start FastAPI server in background
printf "${YELLOW}1. Starting FastAPI server...${NC}\n"
uvicorn main:app --reload --port $PORT &
UVICORN_PID=$!

# Wait a moment for server to start
sleep 5

# Check if FastAPI server started successfully
if ! curl -s http://localhost:$PORT > /dev/null; then
    printf "${RED}Error: FastAPI server failed to start${NC}\n"
    printf "Checking if uvicorn process is running...\n"
    if ! ps aux | grep -q "[u]vicorn"; then
        printf "${RED}uvicorn process not found${NC}\n"
        exit 1
    fi
fi
printf "${GREEN}✓ FastAPI server running on http://localhost:$PORT${NC}\n"

# 2. Start ngrok tunnel in background
printf "${YELLOW}2. Starting ngrok tunnel...${NC}\n"
ngrok http $PORT --log=stdout &
NGROK_PID=$!

# Wait for ngrok to establish tunnel
printf "Waiting for ngrok tunnel to be established...\n"
sleep 10

# Get ngrok URL
NGROK_URL=""
for i in {1..20}; do
    # Try both possible web interface ports (4040 and 4041)
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o 'https://[^"]*\.ngrok[^"]*' | head -n1)
    if [ -z "$NGROK_URL" ]; then
        NGROK_URL=$(curl -s http://localhost:4041/api/tunnels 2>/dev/null | grep -o 'https://[^"]*\.ngrok[^"]*' | head -n1)
    fi
    if [ ! -z "$NGROK_URL" ]; then
        break
    fi
    printf "Waiting for ngrok... (attempt %d/20)\n" "$i"
    sleep 2
done

if [ -z "$NGROK_URL" ]; then
    printf "${RED}Error: Could not get ngrok URL${NC}\n"
    exit 1
fi

printf "${GREEN}✓ ngrok tunnel established: %s${NC}\n" "$NGROK_URL"

# 3. Set Telegram webhook
printf "${YELLOW}3. Setting up Telegram webhook...${NC}\n"
WEBHOOK_URL="$NGROK_URL/webhook"

RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/setWebhook" \
     -d "url=$WEBHOOK_URL")

if echo "$RESPONSE" | grep -q '"ok":true'; then
    printf "${GREEN}✓ Webhook set successfully: %s${NC}\n" "$WEBHOOK_URL"
else
    printf "${RED}Error setting webhook: %s${NC}\n" "$RESPONSE"
    exit 1
fi

printf "\n${GREEN}🚀 Bot is now running!${NC}\n"
printf "FastAPI server: http://localhost:$PORT\n"
printf "Public URL: %s\n" "$NGROK_URL"
printf "Webhook: %s\n" "$WEBHOOK_URL"
printf "\n${YELLOW}Press Ctrl+C to stop the bot${NC}\n"

# Keep script running
wait
