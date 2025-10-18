#!/usr/bin/python

import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

# Import logging configuration FIRST
from src.logging_config import setup_logging, get_logger

load_dotenv()

def setup_logging_from_env():
    """Setup logging from environment variables."""
    setup_logging(
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=os.getenv("LOG_FILE", "bot.log"),
        log_to_console=os.getenv("LOG_TO_CONSOLE", "true").lower() == "true",
        log_to_file=os.getenv("LOG_TO_FILE", "true").lower() == "true",
        json_format=os.getenv("LOG_JSON_FORMAT", "false").lower() == "true",
    )
    
# Get logger for this module
logger = get_logger(__name__)


from src.bot_handler import BotHandler
from src.version import __version__

async def main():
    """Main entry point for the Telegram bot."""
    logger.info("=" * 60)
    logger.info(f"Starting Telegram AI Chat Bot v{__version__}")
    logger.info("=" * 60)
    
    try:
        # Initialize and start bot
        bot_handler = BotHandler()
        logger.info("Bot handler initialized successfully")
        
        # Start polling
        logger.info("Starting bot polling...")
        await bot_handler.start_polling()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (Ctrl+C)")
    except Exception as e:
        logger.critical(f"Fatal error in main: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)