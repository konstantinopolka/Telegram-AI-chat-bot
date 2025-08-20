"""
Bot instance module to avoid circular imports
"""
import os
import logging
import json
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

load_dotenv()
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    logger.error("TELEGRAM_TOKEN not found in environment variables")
    raise ValueError("TELEGRAM_TOKEN is required")

# Create the bot instance with detailed logging
bot = AsyncTeleBot(TOKEN)

# Add middleware to log all incoming updates
@bot.middleware_handler(update_types=['message'])
async def log_incoming_messages(bot_instance, message):
    """Log all incoming messages in detail"""
    update_data = {
        'message_id': message.message_id,
        'from': {
            'id': message.from_user.id,
            'is_bot': message.from_user.is_bot,
            'first_name': message.from_user.first_name,
            'username': getattr(message.from_user, 'username', None),
            'language_code': getattr(message.from_user, 'language_code', None)
        },
        'chat': {
            'id': message.chat.id,
            'first_name': getattr(message.chat, 'first_name', None),
            'username': getattr(message.chat, 'username', None),
            'type': message.chat.type
        },
        'date': message.date,
        'text': getattr(message, 'text', None),
        'content_type': message.content_type
    }
    
    logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")

# Override the reply_to method to log outgoing messages
original_reply_to = bot.reply_to

async def logged_reply_to(message, text, **kwargs):
    """Wrapper for reply_to that logs the response"""
    try:
        result = await original_reply_to(message, text, **kwargs)
        
        if hasattr(result, 'message_id'):
            response_data = {
                'ok': True,
                'result': {
                    'message_id': result.message_id,
                    'from': {
                        'id': result.from_user.id,
                        'is_bot': result.from_user.is_bot,
                        'first_name': result.from_user.first_name,
                        'username': getattr(result.from_user, 'username', None)
                    },
                    'chat': {
                        'id': result.chat.id,
                        'first_name': getattr(result.chat, 'first_name', None),
                        'username': getattr(result.chat, 'username', None),
                        'type': result.chat.type
                    },
                    'date': result.date,
                    'text': result.text
                }
            }
            logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
        
        return result
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        raise

# Replace the bot's reply_to method with our logged version
bot.reply_to = logged_reply_to

logger.info("Bot instance created successfully with detailed logging")
