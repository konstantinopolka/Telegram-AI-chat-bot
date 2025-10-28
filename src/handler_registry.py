import json
from src.dao.models import User, Review
from src.dao.repositories import user_repository, review_repository
from telebot.async_telebot import AsyncTeleBot


from src.logging_config import get_logger

logger = get_logger(__name__)

from src.dao import user_repository

class HandlerRegistry:
    """
    A class that manages and registers all bot message handlers.
    This separates handler registration logic from the main BotHandler class.
    """
    
    def __init__(self, bot):
        """
        Initialize the registry with bot instance and optional logger
        
        Args:
            bot: The AsyncTeleBot instance
            passed_logger: Optional logger instance (deprecated, uses module logger)
        """
        self.bot : AsyncTeleBot = bot
        
        # Create the logged message handler decorator
        self.logged_message_handler = self._create_logged_message_handler()
        
        # Register all handlers when the registry is created
        self.register_all_handlers()
    
    def _create_logged_message_handler(self):
        """Creates a decorator that adds logging to message handlers"""
        def logged_message_handler(**kwargs):
            def decorator(handler_func):
                async def wrapper(message):
                    # Log incoming message
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
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def register_all_handlers(self):
        """Register all message handlers"""
        logger.info("Registering all message handlers")
        logger.debug("Registering welcome/start handler")
        self._register_welcome_handler()
        logger.debug("Registering rules handler")
        self._register_rules_handler()
        logger.debug("Registering review-reposting handler")
        self._register_review_handler()
        logger.debug("Registering echo handler (must be last - catches all messages)")
        self._register_echo_handler()
        
        logger.info("All handlers registered successfully")
    
    def _register_welcome_handler(self):
        """Register welcome/start command handler"""
        logger.debug("Creating welcome command handler for /help and /start")
        
        @self.logged_message_handler(commands=['help', 'start'])
        async def send_welcome(message):
            logger.info(f"Welcome command received from user_id={message.from_user.id}")
            try:
                user: User = await user_repository.get_by_telegram_id(message.from_user.id)
                
                if not user:
                    user = User(
                        telegram_id=message.from_user.id,
                        username=message.from_user.username,
                        first_name=message.from_user.first_name,
                        last_name=getattr(message.from_user, 'last_name', None),
                        phone=None
                    )
                    user = await user_repository.save(user)
                    await self.bot.reply_to(message, "Welcome, you have been registered!")
                else:
                    username = message.from_user.username or message.from_user.first_name or "User"
                    await self.bot.reply_to(message, f"Welcome back, {username}")
                    logger.debug("Welcome back message sent")
                    
            except Exception as e:
                logger.error(f"Error in send_welcome handler: {e}", exc_info=True)
                try:
                    await self.bot.reply_to(message, "Sorry, something went wrong. Please try again.")
                except Exception as reply_error:
                    logger.error(f"Failed to send error message: {reply_error}", exc_info=True)
    
    def _register_rules_handler(self):
        """Register rules command handler"""
        logger.debug("Creating rules command handler for /rules")
        
        @self.logged_message_handler(commands=['rules'])
        async def send_rules(message):
            logger.info(f"Rules command received from user_id={message.from_user.id}")
            try:
                logger.debug("Preparing rules text")
                text = 'Bot rules:\n1. Be respectful\n2. No spam\n3. Have fun!'
                logger.debug(f"Sending rules to user {message.from_user.id}")
                await self.bot.reply_to(message, text)
                logger.info("Rules command processed successfully")
            except Exception as e:
                logger.error(f"Error in send_rules handler: {e}", exc_info=True)
                try:
                    await self.bot.reply_to(message, "Sorry, something went wrong. Please try again.")
                except Exception as reply_error:
                    logger.error(f"Failed to send error message: {reply_error}", exc_info=True)
    
    def _register_review_handler(self):
        """Register review command handler"""
        logger.debug("Creating review command handler for /review")
        
        @self.logged_message_handler(commands=['review'])
        async def review_command(message):
            logger.info(f"Review command received from user_id={message.from_user.id}")
            try:
                # Parse: /review 153 or /review July
                parts = message.text.split(maxsplit=1)
                if len(parts) < 2:
                    await self.bot.reply_to(message, "Usage: /review <id or month>")
                    return
                
                query = parts[1]
                review = None
                
                # Try numeric ID first
                if query.isdigit():
                    review: Review = await review_repository.get_with_articles(int(query))
                else:
                    # Search by month/keyword
                    # TO-DO: add searching by months and years
                    pass 
                
                if review:
                    await self._send_review_to_user(message.chat.id, review)
                else:
                    await self.bot.reply_to(message, f"Review not found: {query}")
                    logger.warning(f"Review not found for query: {query}")
            except Exception as e:
                logger.error(f"Error in review_command handler: {e}", exc_info=True)
                try:
                    await self.bot.reply_to(message, "Sorry, something went wrong. Please try again.")
                except Exception as reply_error:
                    logger.error(f"Failed to send error message: {reply_error}", exc_info=True)
    
    async def _send_review_to_user(self, chat_id: int, review: Review):
        """
        Send a review with Telegraph URLs to a specific user.
        
        Args:
            chat_id: Telegram chat ID to send the message to
            review: Review object containing articles with Telegraph URLs
        """
        logger.info(f"Sending review #{review.id} to chat_id={chat_id}")
        try:
            message_text = self._format_review_message(review)
            await self.bot.send_message(chat_id, message_text, parse_mode='HTML')
            logger.info(f"Review #{review.id} sent successfully to chat_id={chat_id}")
        except Exception as e:
            logger.error(f"Failed to send review #{review.id} to chat_id={chat_id}: {e}", exc_info=True)
            # Try to send error message without HTML parsing
            try:
                await self.bot.send_message(chat_id, "Sorry, failed to load review details.")
            except Exception as fallback_error:
                logger.error(f"Failed to send fallback message: {fallback_error}", exc_info=True)
    
    def _format_review_message(self, review: Review) -> str:
        """
        Format a review into a Telegram message with Telegraph URLs.
        
        Args:
            review: Review object with articles
            
        Returns:
            Formatted HTML message string
        """
        logger.debug(f"Formatting review #{review.id} message")
        
        lines = [f"📰 <b>Review #{review.id}</b>\n"]
        
        if not review.articles or len(review.articles) == 0:
            lines.append("⚠️ No articles found in this review.")
            logger.warning(f"Review #{review.id} has no articles")
        else:
            lines.append(f"📚 <b>{len(review.articles)} article(s):</b>\n")
            
            for idx, article in enumerate(review.articles, 1):
                lines.append(f"{idx}. <b>{article.title}</b>")
                
                # Add Telegraph URLs if available
                if article.telegraph_urls and len(article.telegraph_urls) > 0:
                    # Add all Telegraph URLs
                    lines.extend([f"   📎 <a href='{url}'>Telegraph</a>" for url in article.telegraph_urls])
                else:
                    lines.append("   ⚠️ No Telegraph URLs available")
                
                # Add original URL and spacing
                lines.extend([
                    f"   🔗 <a href='{article.original_url}'>Original article</a>",
                    ""  # Empty line for spacing
                ])
        
        # Add source URL
        lines.append(f"\n📖 <a href='{review.source_url}'>View source review</a>")
        
        formatted_message = "\n".join(lines)
        logger.debug(f"Review message formatted, length: {len(formatted_message)} chars")
        
        return formatted_message
    
    def _register_echo_handler(self):
        """Register echo message handler"""
        logger.debug("Creating echo message handler (catches all messages)")
        
        @self.logged_message_handler(func=lambda message: True)
        async def echo_message(message):
            logger.info(f"Echo handler triggered by user_id={message.from_user.id}")
            try:
                if message.text:  # Only handle text messages
                    logger.debug(f"Text message received: '{message.text[:50]}...'")
                    logger.debug("Echoing message back to user")
                    await self.bot.reply_to(message, f"You said: {message.text}")
                    logger.info("Echo message processed successfully")
                else:
                    logger.debug(f"Non-text message received, type: {message.content_type}")
                    await self.bot.reply_to(message, "I can only echo text messages!")
                    logger.info("Non-text message handled")
            except Exception as e:
                logger.error(f"Error in echo_message handler: {e}", exc_info=True)
                try:
                    await self.bot.reply_to(message, "Sorry, something went wrong. Please try again.")
                except Exception as reply_error:
                    logger.error(f"Failed to send error message: {reply_error}", exc_info=True)
    
    def add_custom_handler(self, decorator_kwargs, handler_func):
        """
        Utility method to add custom handlers dynamically
        
        Args:
            decorator_kwargs: Arguments for the logged_message_handler decorator
            handler_func: The async handler function
        """
        return self.logged_message_handler(**decorator_kwargs)(handler_func)
