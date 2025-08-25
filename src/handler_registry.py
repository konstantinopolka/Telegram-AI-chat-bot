import logging
import json
from src.dao.models import User, AsyncSessionLocal


class HandlerRegistry:
    """
    A class that manages and registers all bot message handlers.
    This separates handler registration logic from the main BotHandler class.
    """
    
    def __init__(self, bot, logger):
        """
        Initialize the registry with bot instance and logger
        
        Args:
            bot: The AsyncTeleBot instance
            logger: Logger instance for this registry
        """
        self.bot = bot
        self.logger = logger
        
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
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def register_all_handlers(self):
        """Register all message handlers"""
        self._register_welcome_handler()
        self._register_rules_handler()
        self._register_echo_handler()
    
    def _register_welcome_handler(self):
        """Register welcome/start command handler"""
        
        @self.logged_message_handler(commands=['help', 'start'])
        async def send_welcome(message):
            try:
                async with AsyncSessionLocal() as session:
                    self.logger.info(f"Processing welcome command from user {message.from_user.id}")
                    user = await session.get(User, message.from_user.id)
                    if not user:
                        user = User(
                            telegram_id=message.from_user.id,
                            username=message.from_user.username,
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                        )
                        session.add(user)
                        await session.commit()
                        await self.bot.reply_to(message, "Welcome, you have been registered!")
                        self.logger.info("New user registered and welcomed.")
                    else:
                        await self.bot.reply_to(message, f"Welcome back, {message.from_user.username}")
                        self.logger.info("Returning user welcomed.")
            except Exception as e:
                self.logger.error(f"Error in send_welcome: {e}", exc_info=True)
                try:
                    await self.bot.reply_to(message, "Sorry, something went wrong. Please try again.")
                except Exception as reply_error:
                    self.logger.error(f"Failed to send error message: {reply_error}")
    
    def _register_rules_handler(self):
        """Register rules command handler"""
        
        @self.logged_message_handler(commands=['rules'])
        async def send_rules(message):
            try:
                self.logger.info(f"Processing rules command from user {message.from_user.id}")
                text = 'Bot rules:\n1. Be respectful\n2. No spam\n3. Have fun!'
                await self.bot.reply_to(message, text)
                self.logger.info("Rules command processed successfully")
            except Exception as e:
                self.logger.error(f"Error in send_rules: {e}", exc_info=True)
                try:
                    await self.bot.reply_to(message, "Sorry, something went wrong. Please try again.")
                except Exception as reply_error:
                    self.logger.error(f"Failed to send error message: {reply_error}")
    
    def _register_echo_handler(self):
        """Register echo message handler"""
        
        @self.logged_message_handler(func=lambda message: True)
        async def echo_message(message):
            try:
                if message.text:  # Only handle text messages
                    self.logger.info(f"Processing echo message from user {message.from_user.id}")
                    await self.bot.reply_to(message, f"You said: {message.text}")
                    self.logger.info("Echo message processed successfully")
                else:
                    self.logger.info(f"Processing non-text message from user {message.from_user.id}")
                    await self.bot.reply_to(message, "I can only echo text messages!")
            except Exception as e:
                self.logger.error(f"Error in echo_message: {e}", exc_info=True)
                try:
                    await self.bot.reply_to(message, "Sorry, something went wrong. Please try again.")
                except Exception as reply_error:
                    self.logger.error(f"Failed to send error message: {reply_error}")
    
    def add_custom_handler(self, decorator_kwargs, handler_func):
        """
        Utility method to add custom handlers dynamically
        
        Args:
            decorator_kwargs: Arguments for the logged_message_handler decorator
            handler_func: The async handler function
        """
        return self.logged_message_handler(**decorator_kwargs)(handler_func)
