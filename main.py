from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    print("Received update:", data)
    return {"ok": True}



BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
print(BOT_TOKEN)