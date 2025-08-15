# Telegram Echo Bot (FastAPI)

This is a simple Telegram bot built with **FastAPI** that echoes back any message sent by the user.

## Features

* Receives messages from a Telegram bot via a webhook.
* Sends back a reply with the same text prefixed by `You said:`.

## Requirements

* Python 3.8+
* A Telegram bot token from [BotFather](https://t.me/BotFather)
* [ngrok](https://ngrok.com/) or another tunneling service for local development

## Installation

1. Clone this repository.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```env
TELEGRAM_TOKEN=your_telegram_bot_token_here
```

## Usage

1. Run the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

2. Expose your server to the internet (for example, with ngrok):

```bash
ngrok http 8000
```

3. Set your Telegram webhook:

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook" \
     -d "url=https://<your-ngrok-url>/webhook"
```

4. Send a message to your bot in Telegram — it will reply with `You said: <your message>`.

### 5. Test the bot

* Open your bot in Telegram.
* Send any message to it.
* You should see logs in your console.


## File Overview

* **main.py** — contains the FastAPI app and logic for receiving and sending Telegram messages.
* **.env** — stores your bot token securely.

## Example Interaction

**User:** Hello!

**Bot:** You said: Hello!

---

**Note:** Do not share your `.env` file or bot token publicly.


## Next Steps

* Implement message-sending functionality.
* Add custom commands and responses.

