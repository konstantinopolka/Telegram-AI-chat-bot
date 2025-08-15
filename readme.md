# Telegram Bot Setup and Usage Guide

This guide explains how to run and use the bot in its current state.

## Requirements

* Python 3.x
* `ngrok` installed
* A Telegram bot token (from [@BotFather](https://t.me/BotFather))

## Setup Steps

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the bot locally

```bash
python main.py
```

### 3. Expose local server with ngrok

If your bot runs on `localhost:8000`:

```bash
ngrok http 8000
```

Copy the generated HTTPS URL (e.g., `https://abc123.ngrok.io`).

### 4. Set the Telegram webhook

Replace `<YOUR_TOKEN>` and `<NGROK_URL>` with your bot token and the copied ngrok URL.

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook" \
     -d "url=<NGROK_URL>/webhook"
```

### 5. Test the bot

* Open your bot in Telegram.
* Send any message to it.
* You should see logs in your console.

## Current Functionality

* The bot receives messages from users and logs them to the console.
* It does not yet send messages back to users.

## Next Steps

* Implement message-sending functionality.
* Add custom commands and responses.
