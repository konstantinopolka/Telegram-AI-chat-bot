import os
import json
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from src.handler_registry import HandlerRegistry
from src.logging_config import get_logger

"""
Bot handler class with object-oriented design
"""

logger = get_logger(__name__)


class BotHandler:
    
    def __init__(self):
        logger.info("Initializing BotHandler")
        logger.debug("Loading environment variables")
        load_dotenv()
        self.logger = logger
        
        logger.debug("Reading TELEGRAM_TOKEN from environment")
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")
        
        logger.debug(f"Token loaded: {TOKEN[:10]}...")
        logger.info("Creating AsyncTeleBot instance")
        
        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        logger.debug("AsyncTeleBot instance created")
        self.handler_registry: HandlerRegistry = None
       
        
        # Setup logging for the bot
        logger.info("Setting up bot message logging wrapper")
        self._setup_bot_logging()
        logger.debug("Bot logging wrapper configured")
        
        # Register all handlers
        logger.info("Registering message handlers")
        self._register_handlers()
        logger.debug("All handlers registered")
        
        logger.info("=" * 60)
        logger.info("BotHandler initialized successfully")
        logger.info("=" * 60)
    
    def _setup_bot_logging(self):
        """Setup logging wrapper for bot messages"""
        logger.debug("Storing original bot.reply_to method")
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            logger.debug(f"Sending reply to chat_id={message.chat.id}")
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
                logger.error(f"Failed to send message: {e}", exc_info=True)
                raise

        # Replace the bot's reply_to method with our logged version
        logger.debug("Replacing bot.reply_to with logged version")
        self.bot.reply_to = logged_reply_to
    
    def _register_handlers(self):
        """Register all message handlers using HandlerRegistry"""
        logger.debug("Creating HandlerRegistry instance")
        # Create the handler registry - it will automatically register all handlers
        self.handler_registry = HandlerRegistry(self.bot, self.logger)
        logger.info(f"HandlerRegistry created and handlers registered")
    
    async def start_polling(self):
        """Start the bot polling"""
        logger.info("Starting bot polling loop")
        logger.info("Bot is now listening for messages...")
        await self.bot.polling(none_stop=True)
        
    async def list_articles(self, user_id: int):
        """
        Show user list of all articles with read/unread status
        """
        pass

    async def read_article(self, user_id: int, article_id: int):
        """
        Show content of a single article, resume from last read position
        """
        pass

    async def mark_progress(self, user_id: int, article_id: int, position: int):
        """
        Save progress for user in the DB
        """
        pass
