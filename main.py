#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import asyncio
import logging
import sys
from dotenv import load_dotenv
import os
from src.bot_handler.bot_handler import BotHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def main():
    """Main function with proper exception handling"""
    try:
        logger.info("Starting bot...")
        bot_handler = BotHandler()
        await bot_handler.start_polling()
        
    except Exception as e:
        logger.error(f"Critical error in bot polling: {e}", exc_info=True)
        raise
    finally:
        logger.info("Bot stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)