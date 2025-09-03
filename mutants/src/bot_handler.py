import os
import logging
import json
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from src.handler_registry import HandlerRegistry

"""
Bot handler class with object-oriented design
"""
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class BotHandler:
    
    def xǁBotHandlerǁ__init____mutmut_orig(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_1(self):
        load_dotenv()
        self.logger = None
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_2(self):
        load_dotenv()
        self.logger = logging.getLogger(None)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_3(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = None
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_4(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv(None)
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_5(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("XXTELEGRAM_TOKENXX")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_6(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("telegram_token")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_7(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_8(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error(None)
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_9(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("XXTELEGRAM_TOKEN not found in environment variablesXX")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_10(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("telegram_token not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_11(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN NOT FOUND IN ENVIRONMENT VARIABLES")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_12(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError(None)

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_13(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("XXTELEGRAM_TOKEN is requiredXX")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_14(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("telegram_token is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_15(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN IS REQUIRED")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_16(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = None
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_17(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(None)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BotHandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_18(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info(None)
    
    def xǁBotHandlerǁ__init____mutmut_19(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("XXBotHandler initialized successfullyXX")
    
    def xǁBotHandlerǁ__init____mutmut_20(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("bothandler initialized successfully")
    
    def xǁBotHandlerǁ__init____mutmut_21(self):
        load_dotenv()
        self.logger = logging.getLogger(__name__)
        
        TOKEN = os.getenv("TELEGRAM_TOKEN")
        if not TOKEN:
            self.logger.error("TELEGRAM_TOKEN not found in environment variables")
            raise ValueError("TELEGRAM_TOKEN is required")

        # Create the bot instance
        self.bot = AsyncTeleBot(TOKEN)
        
        # Setup logging for the bot
        self._setup_bot_logging()
        
        # Register all handlers
        self._register_handlers()
        
        self.logger.info("BOTHANDLER INITIALIZED SUCCESSFULLY")
    
    xǁBotHandlerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBotHandlerǁ__init____mutmut_1': xǁBotHandlerǁ__init____mutmut_1, 
        'xǁBotHandlerǁ__init____mutmut_2': xǁBotHandlerǁ__init____mutmut_2, 
        'xǁBotHandlerǁ__init____mutmut_3': xǁBotHandlerǁ__init____mutmut_3, 
        'xǁBotHandlerǁ__init____mutmut_4': xǁBotHandlerǁ__init____mutmut_4, 
        'xǁBotHandlerǁ__init____mutmut_5': xǁBotHandlerǁ__init____mutmut_5, 
        'xǁBotHandlerǁ__init____mutmut_6': xǁBotHandlerǁ__init____mutmut_6, 
        'xǁBotHandlerǁ__init____mutmut_7': xǁBotHandlerǁ__init____mutmut_7, 
        'xǁBotHandlerǁ__init____mutmut_8': xǁBotHandlerǁ__init____mutmut_8, 
        'xǁBotHandlerǁ__init____mutmut_9': xǁBotHandlerǁ__init____mutmut_9, 
        'xǁBotHandlerǁ__init____mutmut_10': xǁBotHandlerǁ__init____mutmut_10, 
        'xǁBotHandlerǁ__init____mutmut_11': xǁBotHandlerǁ__init____mutmut_11, 
        'xǁBotHandlerǁ__init____mutmut_12': xǁBotHandlerǁ__init____mutmut_12, 
        'xǁBotHandlerǁ__init____mutmut_13': xǁBotHandlerǁ__init____mutmut_13, 
        'xǁBotHandlerǁ__init____mutmut_14': xǁBotHandlerǁ__init____mutmut_14, 
        'xǁBotHandlerǁ__init____mutmut_15': xǁBotHandlerǁ__init____mutmut_15, 
        'xǁBotHandlerǁ__init____mutmut_16': xǁBotHandlerǁ__init____mutmut_16, 
        'xǁBotHandlerǁ__init____mutmut_17': xǁBotHandlerǁ__init____mutmut_17, 
        'xǁBotHandlerǁ__init____mutmut_18': xǁBotHandlerǁ__init____mutmut_18, 
        'xǁBotHandlerǁ__init____mutmut_19': xǁBotHandlerǁ__init____mutmut_19, 
        'xǁBotHandlerǁ__init____mutmut_20': xǁBotHandlerǁ__init____mutmut_20, 
        'xǁBotHandlerǁ__init____mutmut_21': xǁBotHandlerǁ__init____mutmut_21
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBotHandlerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁBotHandlerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁBotHandlerǁ__init____mutmut_orig)
    xǁBotHandlerǁ__init____mutmut_orig.__name__ = 'xǁBotHandlerǁ__init__'
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_orig(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_1(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = None

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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_2(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = None
                
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_3(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(None, text, **kwargs)
                
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_4(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, None, **kwargs)
                
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_5(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(text, **kwargs)
                
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_6(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, **kwargs)
                
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_7(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, )
                
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_8(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(None, 'message_id'):
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_9(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, None):
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_10(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr('message_id'):
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_11(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, ):
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_12(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, 'XXmessage_idXX'):
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_13(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, 'MESSAGE_ID'):
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_14(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, 'message_id'):
                    response_data = None
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_15(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, 'message_id'):
                    response_data = {
                        'XXokXX': True,
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_16(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, 'message_id'):
                    response_data = {
                        'OK': True,
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_17(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, 'message_id'):
                    response_data = {
                        'ok': False,
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_18(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, 'message_id'):
                    response_data = {
                        'ok': True,
                        'XXresultXX': {
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_19(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, 'message_id'):
                    response_data = {
                        'ok': True,
                        'RESULT': {
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_20(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, 'message_id'):
                    response_data = {
                        'ok': True,
                        'result': {
                            'XXmessage_idXX': result.message_id,
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_21(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, 'message_id'):
                    response_data = {
                        'ok': True,
                        'result': {
                            'MESSAGE_ID': result.message_id,
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_22(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, 'message_id'):
                    response_data = {
                        'ok': True,
                        'result': {
                            'message_id': result.message_id,
                            'XXfromXX': {
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_23(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

        async def logged_reply_to(message, text, **kwargs):
            """Wrapper for reply_to that logs the response"""
            try:
                result = await original_reply_to(message, text, **kwargs)
                
                if hasattr(result, 'message_id'):
                    response_data = {
                        'ok': True,
                        'result': {
                            'message_id': result.message_id,
                            'FROM': {
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_24(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'XXidXX': result.from_user.id,
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_25(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'ID': result.from_user.id,
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_26(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'XXis_botXX': result.from_user.is_bot,
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_27(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'IS_BOT': result.from_user.is_bot,
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_28(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'XXfirst_nameXX': result.from_user.first_name,
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_29(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'FIRST_NAME': result.from_user.first_name,
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_30(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'XXusernameXX': getattr(result.from_user, 'username', None)
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_31(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'USERNAME': getattr(result.from_user, 'username', None)
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_32(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr(None, 'username', None)
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_33(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr(result.from_user, None, None)
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_34(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr('username', None)
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_35(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr(result.from_user, None)
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_36(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr(result.from_user, 'username', )
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_37(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr(result.from_user, 'XXusernameXX', None)
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_38(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr(result.from_user, 'USERNAME', None)
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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_39(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                            'XXchatXX': {
                                'id': result.chat.id,
                                'first_name': getattr(result.chat, 'first_name', None),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_40(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                            'CHAT': {
                                'id': result.chat.id,
                                'first_name': getattr(result.chat, 'first_name', None),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_41(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'XXidXX': result.chat.id,
                                'first_name': getattr(result.chat, 'first_name', None),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_42(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'ID': result.chat.id,
                                'first_name': getattr(result.chat, 'first_name', None),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_43(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'XXfirst_nameXX': getattr(result.chat, 'first_name', None),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_44(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'FIRST_NAME': getattr(result.chat, 'first_name', None),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_45(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'first_name': getattr(None, 'first_name', None),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_46(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'first_name': getattr(result.chat, None, None),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_47(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'first_name': getattr('first_name', None),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_48(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'first_name': getattr(result.chat, None),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_49(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'first_name': getattr(result.chat, 'first_name', ),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_50(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'first_name': getattr(result.chat, 'XXfirst_nameXX', None),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_51(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'first_name': getattr(result.chat, 'FIRST_NAME', None),
                                'username': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_52(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'XXusernameXX': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_53(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'USERNAME': getattr(result.chat, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_54(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr(None, 'username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_55(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr(result.chat, None, None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_56(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr('username', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_57(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr(result.chat, None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_58(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr(result.chat, 'username', ),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_59(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr(result.chat, 'XXusernameXX', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_60(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'username': getattr(result.chat, 'USERNAME', None),
                                'type': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_61(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'XXtypeXX': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_62(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                                'TYPE': result.chat.type
                            },
                            'date': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_63(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                            'XXdateXX': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_64(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                            'DATE': result.date,
                            'text': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_65(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                            'XXtextXX': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_66(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                            'TEXT': result.text
                        }
                    }
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_67(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                    self.logger.info(None)
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_68(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                    self.logger.info(f"Sent: {json.dumps(None, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_69(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=None, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_70(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=None)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_71(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                    self.logger.info(f"Sent: {json.dumps(ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_72(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                    self.logger.info(f"Sent: {json.dumps(response_data, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_73(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, )}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_74(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=True, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_75(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=3)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_76(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(None)
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = logged_reply_to
    
    def xǁBotHandlerǁ_setup_bot_logging__mutmut_77(self):
        """Setup logging wrapper for bot messages"""
        # Store the original reply_to method
        original_reply_to = self.bot.reply_to

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
                    self.logger.info(f"Sent: {json.dumps(response_data, ensure_ascii=False, indent=2)}")
                
                return result
            except Exception as e:
                self.logger.error(f"Failed to send message: {e}")
                raise

        # Replace the bot's reply_to method with our logged version
        self.bot.reply_to = None
    
    xǁBotHandlerǁ_setup_bot_logging__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBotHandlerǁ_setup_bot_logging__mutmut_1': xǁBotHandlerǁ_setup_bot_logging__mutmut_1, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_2': xǁBotHandlerǁ_setup_bot_logging__mutmut_2, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_3': xǁBotHandlerǁ_setup_bot_logging__mutmut_3, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_4': xǁBotHandlerǁ_setup_bot_logging__mutmut_4, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_5': xǁBotHandlerǁ_setup_bot_logging__mutmut_5, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_6': xǁBotHandlerǁ_setup_bot_logging__mutmut_6, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_7': xǁBotHandlerǁ_setup_bot_logging__mutmut_7, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_8': xǁBotHandlerǁ_setup_bot_logging__mutmut_8, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_9': xǁBotHandlerǁ_setup_bot_logging__mutmut_9, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_10': xǁBotHandlerǁ_setup_bot_logging__mutmut_10, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_11': xǁBotHandlerǁ_setup_bot_logging__mutmut_11, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_12': xǁBotHandlerǁ_setup_bot_logging__mutmut_12, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_13': xǁBotHandlerǁ_setup_bot_logging__mutmut_13, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_14': xǁBotHandlerǁ_setup_bot_logging__mutmut_14, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_15': xǁBotHandlerǁ_setup_bot_logging__mutmut_15, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_16': xǁBotHandlerǁ_setup_bot_logging__mutmut_16, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_17': xǁBotHandlerǁ_setup_bot_logging__mutmut_17, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_18': xǁBotHandlerǁ_setup_bot_logging__mutmut_18, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_19': xǁBotHandlerǁ_setup_bot_logging__mutmut_19, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_20': xǁBotHandlerǁ_setup_bot_logging__mutmut_20, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_21': xǁBotHandlerǁ_setup_bot_logging__mutmut_21, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_22': xǁBotHandlerǁ_setup_bot_logging__mutmut_22, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_23': xǁBotHandlerǁ_setup_bot_logging__mutmut_23, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_24': xǁBotHandlerǁ_setup_bot_logging__mutmut_24, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_25': xǁBotHandlerǁ_setup_bot_logging__mutmut_25, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_26': xǁBotHandlerǁ_setup_bot_logging__mutmut_26, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_27': xǁBotHandlerǁ_setup_bot_logging__mutmut_27, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_28': xǁBotHandlerǁ_setup_bot_logging__mutmut_28, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_29': xǁBotHandlerǁ_setup_bot_logging__mutmut_29, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_30': xǁBotHandlerǁ_setup_bot_logging__mutmut_30, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_31': xǁBotHandlerǁ_setup_bot_logging__mutmut_31, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_32': xǁBotHandlerǁ_setup_bot_logging__mutmut_32, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_33': xǁBotHandlerǁ_setup_bot_logging__mutmut_33, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_34': xǁBotHandlerǁ_setup_bot_logging__mutmut_34, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_35': xǁBotHandlerǁ_setup_bot_logging__mutmut_35, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_36': xǁBotHandlerǁ_setup_bot_logging__mutmut_36, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_37': xǁBotHandlerǁ_setup_bot_logging__mutmut_37, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_38': xǁBotHandlerǁ_setup_bot_logging__mutmut_38, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_39': xǁBotHandlerǁ_setup_bot_logging__mutmut_39, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_40': xǁBotHandlerǁ_setup_bot_logging__mutmut_40, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_41': xǁBotHandlerǁ_setup_bot_logging__mutmut_41, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_42': xǁBotHandlerǁ_setup_bot_logging__mutmut_42, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_43': xǁBotHandlerǁ_setup_bot_logging__mutmut_43, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_44': xǁBotHandlerǁ_setup_bot_logging__mutmut_44, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_45': xǁBotHandlerǁ_setup_bot_logging__mutmut_45, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_46': xǁBotHandlerǁ_setup_bot_logging__mutmut_46, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_47': xǁBotHandlerǁ_setup_bot_logging__mutmut_47, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_48': xǁBotHandlerǁ_setup_bot_logging__mutmut_48, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_49': xǁBotHandlerǁ_setup_bot_logging__mutmut_49, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_50': xǁBotHandlerǁ_setup_bot_logging__mutmut_50, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_51': xǁBotHandlerǁ_setup_bot_logging__mutmut_51, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_52': xǁBotHandlerǁ_setup_bot_logging__mutmut_52, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_53': xǁBotHandlerǁ_setup_bot_logging__mutmut_53, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_54': xǁBotHandlerǁ_setup_bot_logging__mutmut_54, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_55': xǁBotHandlerǁ_setup_bot_logging__mutmut_55, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_56': xǁBotHandlerǁ_setup_bot_logging__mutmut_56, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_57': xǁBotHandlerǁ_setup_bot_logging__mutmut_57, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_58': xǁBotHandlerǁ_setup_bot_logging__mutmut_58, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_59': xǁBotHandlerǁ_setup_bot_logging__mutmut_59, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_60': xǁBotHandlerǁ_setup_bot_logging__mutmut_60, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_61': xǁBotHandlerǁ_setup_bot_logging__mutmut_61, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_62': xǁBotHandlerǁ_setup_bot_logging__mutmut_62, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_63': xǁBotHandlerǁ_setup_bot_logging__mutmut_63, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_64': xǁBotHandlerǁ_setup_bot_logging__mutmut_64, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_65': xǁBotHandlerǁ_setup_bot_logging__mutmut_65, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_66': xǁBotHandlerǁ_setup_bot_logging__mutmut_66, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_67': xǁBotHandlerǁ_setup_bot_logging__mutmut_67, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_68': xǁBotHandlerǁ_setup_bot_logging__mutmut_68, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_69': xǁBotHandlerǁ_setup_bot_logging__mutmut_69, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_70': xǁBotHandlerǁ_setup_bot_logging__mutmut_70, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_71': xǁBotHandlerǁ_setup_bot_logging__mutmut_71, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_72': xǁBotHandlerǁ_setup_bot_logging__mutmut_72, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_73': xǁBotHandlerǁ_setup_bot_logging__mutmut_73, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_74': xǁBotHandlerǁ_setup_bot_logging__mutmut_74, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_75': xǁBotHandlerǁ_setup_bot_logging__mutmut_75, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_76': xǁBotHandlerǁ_setup_bot_logging__mutmut_76, 
        'xǁBotHandlerǁ_setup_bot_logging__mutmut_77': xǁBotHandlerǁ_setup_bot_logging__mutmut_77
    }
    
    def _setup_bot_logging(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBotHandlerǁ_setup_bot_logging__mutmut_orig"), object.__getattribute__(self, "xǁBotHandlerǁ_setup_bot_logging__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _setup_bot_logging.__signature__ = _mutmut_signature(xǁBotHandlerǁ_setup_bot_logging__mutmut_orig)
    xǁBotHandlerǁ_setup_bot_logging__mutmut_orig.__name__ = 'xǁBotHandlerǁ_setup_bot_logging'
    
    def xǁBotHandlerǁ_register_handlers__mutmut_orig(self):
        """Register all message handlers using HandlerRegistry"""
        # Create the handler registry - it will automatically register all handlers
        self.handler_registry = HandlerRegistry(self.bot, self.logger)
    
    def xǁBotHandlerǁ_register_handlers__mutmut_1(self):
        """Register all message handlers using HandlerRegistry"""
        # Create the handler registry - it will automatically register all handlers
        self.handler_registry = None
    
    def xǁBotHandlerǁ_register_handlers__mutmut_2(self):
        """Register all message handlers using HandlerRegistry"""
        # Create the handler registry - it will automatically register all handlers
        self.handler_registry = HandlerRegistry(None, self.logger)
    
    def xǁBotHandlerǁ_register_handlers__mutmut_3(self):
        """Register all message handlers using HandlerRegistry"""
        # Create the handler registry - it will automatically register all handlers
        self.handler_registry = HandlerRegistry(self.bot, None)
    
    def xǁBotHandlerǁ_register_handlers__mutmut_4(self):
        """Register all message handlers using HandlerRegistry"""
        # Create the handler registry - it will automatically register all handlers
        self.handler_registry = HandlerRegistry(self.logger)
    
    def xǁBotHandlerǁ_register_handlers__mutmut_5(self):
        """Register all message handlers using HandlerRegistry"""
        # Create the handler registry - it will automatically register all handlers
        self.handler_registry = HandlerRegistry(self.bot, )
    
    xǁBotHandlerǁ_register_handlers__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBotHandlerǁ_register_handlers__mutmut_1': xǁBotHandlerǁ_register_handlers__mutmut_1, 
        'xǁBotHandlerǁ_register_handlers__mutmut_2': xǁBotHandlerǁ_register_handlers__mutmut_2, 
        'xǁBotHandlerǁ_register_handlers__mutmut_3': xǁBotHandlerǁ_register_handlers__mutmut_3, 
        'xǁBotHandlerǁ_register_handlers__mutmut_4': xǁBotHandlerǁ_register_handlers__mutmut_4, 
        'xǁBotHandlerǁ_register_handlers__mutmut_5': xǁBotHandlerǁ_register_handlers__mutmut_5
    }
    
    def _register_handlers(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBotHandlerǁ_register_handlers__mutmut_orig"), object.__getattribute__(self, "xǁBotHandlerǁ_register_handlers__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _register_handlers.__signature__ = _mutmut_signature(xǁBotHandlerǁ_register_handlers__mutmut_orig)
    xǁBotHandlerǁ_register_handlers__mutmut_orig.__name__ = 'xǁBotHandlerǁ_register_handlers'
    
    async def xǁBotHandlerǁstart_polling__mutmut_orig(self):
        """Start the bot polling"""
        await self.bot.polling(none_stop=True)
        
    
    async def xǁBotHandlerǁstart_polling__mutmut_1(self):
        """Start the bot polling"""
        await self.bot.polling(none_stop=None)
        
    
    async def xǁBotHandlerǁstart_polling__mutmut_2(self):
        """Start the bot polling"""
        await self.bot.polling(none_stop=False)
        
    
    xǁBotHandlerǁstart_polling__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁBotHandlerǁstart_polling__mutmut_1': xǁBotHandlerǁstart_polling__mutmut_1, 
        'xǁBotHandlerǁstart_polling__mutmut_2': xǁBotHandlerǁstart_polling__mutmut_2
    }
    
    def start_polling(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁBotHandlerǁstart_polling__mutmut_orig"), object.__getattribute__(self, "xǁBotHandlerǁstart_polling__mutmut_mutants"), args, kwargs, self)
        return result 
    
    start_polling.__signature__ = _mutmut_signature(xǁBotHandlerǁstart_polling__mutmut_orig)
    xǁBotHandlerǁstart_polling__mutmut_orig.__name__ = 'xǁBotHandlerǁstart_polling'
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
