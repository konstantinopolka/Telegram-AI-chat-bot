from fastapi import FastAPI
from fastapi import Request
import requests
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

def send_message(chat_id: int, text: str):
    token = os.getenv("TELEGRAM_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text,
    }

    response = requests.post(url, data=payload)
    print("Sent:", response.json())


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    print("Received update:", data)
    
    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"]["text"]
    
    reply = f"You said: {user_text}"
    send_message(chat_id, reply)

    
    return {"ok": True}




BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
print(BOT_TOKEN)