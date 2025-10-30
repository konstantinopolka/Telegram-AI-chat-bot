import os
import json
from dotenv import load_dotenv
from typing import List, Any, Callable, Optional

from telebot.async_telebot import AsyncTeleBot


from src.handler_registry import HandlerRegistry
from src.logging_config import get_logger
from src.dao.repositories import user_repository
from src.dao.models import User
import asyncio

"""
Bot handler class with object-oriented design
"""

logger = get_logger(__name__)


class BotHandler:
    
    def __init__(self):
        logger.info("Initializing BotHandler")
        logger.debug("Loading environment variables")
        load_dotenv()
        
        logger.debug("Reading TELEGRAM_TOKEN from environment")
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")
        
        logger.debug(f"Token loaded: {TOKEN[:10]}...")
        logger.info("Creating AsyncTeleBot instance")
        
        # Create the bot instance
        self.bot: AsyncTeleBot = AsyncTeleBot(TOKEN)
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
            
            # modification of reply_to -> belongs to MessageService
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
        self.handler_registry = HandlerRegistry(self.bot)
        logger.info(f"HandlerRegistry created and handlers registered")
    
    async def start_polling(self):
        """Start the bot polling"""
        logger.info("Starting bot polling loop")
        logger.info("Bot is now listening for messages...")
        await self.bot.polling(none_stop=True)
    async def broadcast_message(self, message: str, formatting_function: Optional[Callable[[str], str]] = None, parse_mode: str = 'HTML'):
        """Send a message to all users"""
        logger.info("=" * 60)
        logger.info("Starting broadcast_message")
        logger.info(f"Message to broadcast: '{message[:100]}{'...' if len(message) > 100 else ''}'")
        
        # Fetch all users
        logger.debug("Fetching all users from database")
        try:
            users: List[User] = await user_repository.get_all()
            logger.info(f"Retrieved {len(users) if users else 0} users from database")
        except Exception as e:
            logger.error(f"Failed to fetch users from database: {e}", exc_info=True)
            return
        
        
        
        if not users:
            logger.warning("No users to broadcast to - aborting broadcast")
            return
        
        # Log user details
        logger.debug("Users to broadcast to:")
        for idx, user in enumerate(users, 1):
            logger.debug(f"  {idx}. User(id={user.telegram_id}, telegram_id={user.telegram_id}, username={getattr(user, 'username', 'N/A')})")
        
        
        # Apply formatting function if provided
        formatted_message = formatting_function(message) if formatting_function else message
        
        if formatting_function:
            logger.debug(f"Applied formatting function: {formatting_function.__name__ if hasattr(formatting_function, '__name__') else 'lambda'}")
        # Create tasks for all users
        logger.info(f"Creating {len(users)} send tasks")
        tasks = []
        
        for user in users:
            logger.debug(f"Creating task for user telegram_id={user.telegram_id}")
            task = self.user_send_message(user_id=user.telegram_id, message=formatted_message, formatting_function=None, parse_mode=parse_mode)
            tasks.append(task)
        
        logger.info(f"Created {len(tasks)} tasks, executing concurrently with asyncio.gather()")
        
        # Execute all sends concurrently
        try:
            results: List[Any | Exception] = await asyncio.gather(*tasks, return_exceptions=True)
            logger.info(f"asyncio.gather() completed, received {len(results)} results")
        except Exception as e:
            logger.error(f"Unexpected error during asyncio.gather(): {e}", exc_info=True)
            return
        
        # Analyze results
        async def __analyze_gather_results(results: List[Any | Exception], users: List[User]):
            """Analyze the results of broadcast and log success/failure"""
            logger.debug("Analyzing gather results")
            
            # Track success/failure
            success_count = 0
            failure_count = 0
            
            for user, result in zip(users, results):
                if isinstance(result, Exception):
                    logger.error(f"❌ Failed to send to user {user.telegram_id} (username={getattr(user, 'username', 'N/A')}): {result}", exc_info=True)
                    failure_count += 1
                else:
                    logger.debug(f"✓ Successfully sent to user {user.telegram_id} (username={getattr(user, 'username', 'N/A')})")
                    success_count += 1
            
            logger.info("=" * 60)
            logger.info(f"Broadcast complete: {success_count} succeeded, {failure_count} failed")
            logger.info("=" * 60)
        
        await __analyze_gather_results(results, users)
        
    async def user_send_message(self, user_id: int, message: str, formatting_function: Optional[Callable[[str], str]] = None, parse_mode: str = 'HTML'):
        """
        Send a message to a specific user with optional formatting.
        
        Args:
            user_id: Telegram user ID to send message to
            message: Message text to send
            formatting_function: Optional function to format the message before sending.
                            Should accept a string and return a formatted string.
            parse_mode: Telegram parse mode (default: 'HTML')
        
        Returns:
            The sent message object from Telegram API
        """
        
        logger.info(f"Sending message to user_id={user_id}")
        logger.debug(f"Message preview: '{message[:100]}{'...' if len(message) > 100 else ''}'")
        
        
        try:
            # Apply formatting function if provided
            formatted_message = formatting_function(message) if formatting_function else message
            
            if formatting_function:
                logger.debug(f"Applied formatting function: {formatting_function.__name__ if hasattr(formatting_function, '__name__') else 'lambda'}")
            
            # Send the message
            result = await self.bot.send_message(user_id, formatted_message, parse_mode=parse_mode)
            logger.info(f"✓ Message sent successfully to user_id={user_id}")
            return result
        
        except Exception as e:
            logger.error(f"❌ Failed to send message to user_id={user_id}: {e}", exc_info=True)
            raise
        
    async def list_articles(self, user_id: int):
        """
        Show user list of all articles with read/unread status
        """
        pass
