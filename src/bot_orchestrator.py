"""
Bot orchestrator - coordinates bot operations and message handling
"""
import os
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

from src.logging_config import get_logger
from src.message_service import MessageService
from src.handler_registry import HandlerRegistry

logger = get_logger(__name__)


class BotOrchestrator:
    """
    Orchestrates bot components and provides high-level bot operations.
    This class follows the Facade pattern to simplify bot management.
    """
    
    def __init__(self):
        logger.info("Initializing BotOrchestrator")
        logger.debug("Loading environment variables")
        load_dotenv()
        
        # Initialize bot
        logger.debug("Reading TELEGRAM_TOKEN from environment")
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")
        
        logger.debug(f"Token loaded: {TOKEN[:10]}...")
        self.bot: AsyncTeleBot = AsyncTeleBot(TOKEN)
        logger.info("AsyncTeleBot instance created")
        
        # Initialize services
        logger.info("Creating MessageService")
        self.message_service = MessageService(self.bot)
        
        # Initialize handler registry with message service
        logger.info("Creating HandlerRegistry with MessageService")
        self.handler_registry = HandlerRegistry(
            bot=self.bot,
            message_service=self.message_service
        )
        
        logger.info("=" * 60)
        logger.info("BotOrchestrator initialized successfully")
        logger.info("=" * 60)
    
    async def start(self):
        """Start the bot polling"""
        logger.info("Starting bot polling loop")
        logger.info("Bot is now listening for messages...")
        await self.bot.polling(none_stop=True)
    
    async def broadcast_message(self, *args, **kwargs):
        """Delegate to message service"""
        return await self.message_service.broadcast_message(*args, **kwargs)
    
    async def send_message(self, *args, **kwargs):
        """Delegate to message service"""
        return await self.message_service.send_message(*args, **kwargs)