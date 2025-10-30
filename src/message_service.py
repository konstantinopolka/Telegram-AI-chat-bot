"""
Message service - handles all message sending operations
"""
import asyncio
import json
from typing import List, Any, Callable, Optional

from telebot.async_telebot import AsyncTeleBot

from src.logging_config import get_logger
from src.dao.repositories import user_repository
from src.dao.models import User, Review

logger = get_logger(__name__)


class MessageService:
    """
    Service for sending messages to users.
    Handles single messages, broadcasts, and formatting.
    """
    
    def __init__(self, bot: AsyncTeleBot):
        """
        Initialize message service with bot instance.
        
        Args:
            bot: AsyncTeleBot instance for sending messages
        """
        self.bot = bot
        logger.info("Setting up logging the bot's replies")
        self._setup_bot_responses_logging()
        logger.info("MessageService initialized")
        
    
    async def send_message(
        self,
        user_id: int,
        message: str,
        formatting_function: Optional[Callable[[str], str]] = None,
        parse_mode: str = 'HTML'
    ) -> Any:
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
            
        Example:
            # Send plain message
            await message_service.send_message(12345, "Hello!")
            
            # Send with formatting
            await message_service.send_message(
                12345, 
                "Alert",
                formatting_function=lambda msg: f"🚨 <b>{msg}</b>"
            )
        """
        logger.info(f"Sending message to user_id={user_id}")
        logger.debug(f"Message preview: '{message[:100]}{'...' if len(message) > 100 else ''}'")
        
        try:
            # Apply formatting function if provided
            formatted_message = formatting_function(message) if formatting_function else message
            
            if formatting_function:
                logger.debug(
                    f"Applied formatting function: "
                    f"{formatting_function.__name__ if hasattr(formatting_function, '__name__') else 'lambda'}"
                )
            
            # Send the message
            result = await self.bot.send_message(user_id, formatted_message, parse_mode=parse_mode)
            logger.info(f"✓ Message sent successfully to user_id={user_id}")
            return result
        
        except Exception as e:
            logger.error(f"❌ Failed to send message to user_id={user_id}: {e}", exc_info=True)
            raise
    
    async def broadcast_message(
        self,
        message: str,
        formatting_function: Optional[Callable[[str], str]] = None,
        parse_mode: str = 'HTML'
    ):
        """
        Send a message to all users.
        
        Args:
            message: Message text to send
            formatting_function: Optional function to format the message once before broadcasting
            parse_mode: Telegram parse mode (default: 'HTML')
        """
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
            logger.debug(
                f"  {idx}. User(id={user.telegram_id}, telegram_id={user.telegram_id}, "
                f"username={getattr(user, 'username', 'N/A')})"
            )
        
        # Format message ONCE before broadcasting (performance optimization)
        formatted_message = formatting_function(message) if formatting_function else message
        
        if formatting_function:
            logger.debug(
                f"Applied formatting function: "
                f"{formatting_function.__name__ if hasattr(formatting_function, '__name__') else 'lambda'}"
            )
            logger.debug(f"Formatted message preview: '{formatted_message[:100]}{'...' if len(formatted_message) > 100 else ''}'")
        
        # Create tasks for all users - pass pre-formatted message
        logger.info(f"Creating {len(users)} send tasks")
        tasks = []
        
        for user in users:
            logger.debug(f"Creating task for user telegram_id={user.telegram_id}")
            # Pass pre-formatted message, no formatter (already applied)
            task = self.send_message(
                user_id=user.telegram_id,
                message=formatted_message,
                formatting_function=None,  # Don't format again
                parse_mode=parse_mode
            )
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
        await self._analyze_broadcast_results(results, users)
    
    async def _analyze_broadcast_results(self, results: List[Any | Exception], users: List[User]):
        """
        Analyze the results of broadcast and log success/failure.
        
        Args:
            results: List of results from asyncio.gather (Message objects or Exceptions)
            users: List of users that messages were sent to
        """
        logger.debug("Analyzing gather results")
        
        # Track success/failure
        success_count = 0
        failure_count = 0
        
        for user, result in zip(users, results):
            if isinstance(result, Exception):
                logger.error(
                    f"❌ Failed to send to user {user.telegram_id} "
                    f"(username={getattr(user, 'username', 'N/A')}): {result}",
                    exc_info=True
                )
                failure_count += 1
            else:
                logger.debug(
                    f"✓ Successfully sent to user {user.telegram_id} "
                    f"(username={getattr(user, 'username', 'N/A')})"
                )
                success_count += 1
        
        logger.info("=" * 60)
        logger.info(f"Broadcast complete: {success_count} succeeded, {failure_count} failed")
        logger.info("=" * 60)
        
    def _setup_bot_responses_logging(self):
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
        
    async def send_review_to_user(self, chat_id: int, review: Review):
        """
        Send a review with Telegraph URLs to a specific user.
        
        Args:
            chat_id: Telegram chat ID to send the message to
            review: Review object containing articles with Telegraph URLs
        """
        logger.info(f"Sending review #{review.id} to chat_id={chat_id}")
        
        # Use Review's __str__ method for formatting
        message_text = str(review)
        logger.debug(f"Review formatted, message length: {len(message_text)} chars")
        
        # Send the message
        try:
            await self.send_message(
                user_id=chat_id,
                message=message_text,
                formatting_function=None,  # Already formatted by Review.__str__()
                parse_mode='HTML'
            )
            logger.info(f"Review #{review.id} sent successfully to chat_id={chat_id}")
        except Exception as e:
            logger.error(f"Failed to send review #{review.id} to chat_id={chat_id}: {e}", exc_info=True)
            try:
                await self.send_message(user_id=chat_id, message="Sorry, failed to load review details.")
            except Exception as fallback_error:
                logger.error(f"Failed to send fallback message: {fallback_error}", exc_info=True)