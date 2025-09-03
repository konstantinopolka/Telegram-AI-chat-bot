import logging
import json
from src.dao.models import User
from src.dao import AsyncSessionLocal
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


class HandlerRegistry:
    """
    A class that manages and registers all bot message handlers.
    This separates handler registration logic from the main BotHandler class.
    """
    
    def xǁHandlerRegistryǁ__init____mutmut_orig(self, bot, logger):
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
    
    def xǁHandlerRegistryǁ__init____mutmut_1(self, bot, logger):
        """
        Initialize the registry with bot instance and logger
        
        Args:
            bot: The AsyncTeleBot instance
            logger: Logger instance for this registry
        """
        self.bot = None
        self.logger = logger
        
        # Create the logged message handler decorator
        self.logged_message_handler = self._create_logged_message_handler()
        
        # Register all handlers when the registry is created
        self.register_all_handlers()
    
    def xǁHandlerRegistryǁ__init____mutmut_2(self, bot, logger):
        """
        Initialize the registry with bot instance and logger
        
        Args:
            bot: The AsyncTeleBot instance
            logger: Logger instance for this registry
        """
        self.bot = bot
        self.logger = None
        
        # Create the logged message handler decorator
        self.logged_message_handler = self._create_logged_message_handler()
        
        # Register all handlers when the registry is created
        self.register_all_handlers()
    
    def xǁHandlerRegistryǁ__init____mutmut_3(self, bot, logger):
        """
        Initialize the registry with bot instance and logger
        
        Args:
            bot: The AsyncTeleBot instance
            logger: Logger instance for this registry
        """
        self.bot = bot
        self.logger = logger
        
        # Create the logged message handler decorator
        self.logged_message_handler = None
        
        # Register all handlers when the registry is created
        self.register_all_handlers()
    
    xǁHandlerRegistryǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHandlerRegistryǁ__init____mutmut_1': xǁHandlerRegistryǁ__init____mutmut_1, 
        'xǁHandlerRegistryǁ__init____mutmut_2': xǁHandlerRegistryǁ__init____mutmut_2, 
        'xǁHandlerRegistryǁ__init____mutmut_3': xǁHandlerRegistryǁ__init____mutmut_3
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHandlerRegistryǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁHandlerRegistryǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁHandlerRegistryǁ__init____mutmut_orig)
    xǁHandlerRegistryǁ__init____mutmut_orig.__name__ = 'xǁHandlerRegistryǁ__init__'
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_orig(self):
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_1(self):
        """Creates a decorator that adds logging to message handlers"""
        def logged_message_handler(**kwargs):
            def decorator(handler_func):
                async def wrapper(message):
                    # Log incoming message
                    update_data = None
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_2(self):
        """Creates a decorator that adds logging to message handlers"""
        def logged_message_handler(**kwargs):
            def decorator(handler_func):
                async def wrapper(message):
                    # Log incoming message
                    update_data = {
                        'XXmessage_idXX': message.message_id,
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_3(self):
        """Creates a decorator that adds logging to message handlers"""
        def logged_message_handler(**kwargs):
            def decorator(handler_func):
                async def wrapper(message):
                    # Log incoming message
                    update_data = {
                        'MESSAGE_ID': message.message_id,
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_4(self):
        """Creates a decorator that adds logging to message handlers"""
        def logged_message_handler(**kwargs):
            def decorator(handler_func):
                async def wrapper(message):
                    # Log incoming message
                    update_data = {
                        'message_id': message.message_id,
                        'XXfromXX': {
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_5(self):
        """Creates a decorator that adds logging to message handlers"""
        def logged_message_handler(**kwargs):
            def decorator(handler_func):
                async def wrapper(message):
                    # Log incoming message
                    update_data = {
                        'message_id': message.message_id,
                        'FROM': {
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_6(self):
        """Creates a decorator that adds logging to message handlers"""
        def logged_message_handler(**kwargs):
            def decorator(handler_func):
                async def wrapper(message):
                    # Log incoming message
                    update_data = {
                        'message_id': message.message_id,
                        'from': {
                            'XXidXX': message.from_user.id,
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_7(self):
        """Creates a decorator that adds logging to message handlers"""
        def logged_message_handler(**kwargs):
            def decorator(handler_func):
                async def wrapper(message):
                    # Log incoming message
                    update_data = {
                        'message_id': message.message_id,
                        'from': {
                            'ID': message.from_user.id,
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_8(self):
        """Creates a decorator that adds logging to message handlers"""
        def logged_message_handler(**kwargs):
            def decorator(handler_func):
                async def wrapper(message):
                    # Log incoming message
                    update_data = {
                        'message_id': message.message_id,
                        'from': {
                            'id': message.from_user.id,
                            'XXis_botXX': message.from_user.is_bot,
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_9(self):
        """Creates a decorator that adds logging to message handlers"""
        def logged_message_handler(**kwargs):
            def decorator(handler_func):
                async def wrapper(message):
                    # Log incoming message
                    update_data = {
                        'message_id': message.message_id,
                        'from': {
                            'id': message.from_user.id,
                            'IS_BOT': message.from_user.is_bot,
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_10(self):
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
                            'XXfirst_nameXX': message.from_user.first_name,
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_11(self):
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
                            'FIRST_NAME': message.from_user.first_name,
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_12(self):
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
                            'XXusernameXX': getattr(message.from_user, 'username', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_13(self):
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
                            'USERNAME': getattr(message.from_user, 'username', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_14(self):
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
                            'username': getattr(None, 'username', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_15(self):
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
                            'username': getattr(message.from_user, None, None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_16(self):
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
                            'username': getattr('username', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_17(self):
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
                            'username': getattr(message.from_user, None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_18(self):
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
                            'username': getattr(message.from_user, 'username', ),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_19(self):
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
                            'username': getattr(message.from_user, 'XXusernameXX', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_20(self):
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
                            'username': getattr(message.from_user, 'USERNAME', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_21(self):
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
                            'XXlanguage_codeXX': getattr(message.from_user, 'language_code', None)
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_22(self):
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
                            'LANGUAGE_CODE': getattr(message.from_user, 'language_code', None)
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_23(self):
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
                            'language_code': getattr(None, 'language_code', None)
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_24(self):
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
                            'language_code': getattr(message.from_user, None, None)
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_25(self):
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
                            'language_code': getattr('language_code', None)
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_26(self):
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
                            'language_code': getattr(message.from_user, None)
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_27(self):
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
                            'language_code': getattr(message.from_user, 'language_code', )
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_28(self):
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
                            'language_code': getattr(message.from_user, 'XXlanguage_codeXX', None)
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_29(self):
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
                            'language_code': getattr(message.from_user, 'LANGUAGE_CODE', None)
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_30(self):
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
                        'XXchatXX': {
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_31(self):
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
                        'CHAT': {
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_32(self):
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
                            'XXidXX': message.chat.id,
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_33(self):
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
                            'ID': message.chat.id,
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_34(self):
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
                            'XXfirst_nameXX': getattr(message.chat, 'first_name', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_35(self):
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
                            'FIRST_NAME': getattr(message.chat, 'first_name', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_36(self):
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
                            'first_name': getattr(None, 'first_name', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_37(self):
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
                            'first_name': getattr(message.chat, None, None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_38(self):
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
                            'first_name': getattr('first_name', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_39(self):
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
                            'first_name': getattr(message.chat, None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_40(self):
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
                            'first_name': getattr(message.chat, 'first_name', ),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_41(self):
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
                            'first_name': getattr(message.chat, 'XXfirst_nameXX', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_42(self):
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
                            'first_name': getattr(message.chat, 'FIRST_NAME', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_43(self):
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
                            'XXusernameXX': getattr(message.chat, 'username', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_44(self):
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
                            'USERNAME': getattr(message.chat, 'username', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_45(self):
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
                            'username': getattr(None, 'username', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_46(self):
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
                            'username': getattr(message.chat, None, None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_47(self):
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
                            'username': getattr('username', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_48(self):
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
                            'username': getattr(message.chat, None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_49(self):
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
                            'username': getattr(message.chat, 'username', ),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_50(self):
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
                            'username': getattr(message.chat, 'XXusernameXX', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_51(self):
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
                            'username': getattr(message.chat, 'USERNAME', None),
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_52(self):
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
                            'XXtypeXX': message.chat.type
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_53(self):
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
                            'TYPE': message.chat.type
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_54(self):
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
                        'XXdateXX': message.date,
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_55(self):
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
                        'DATE': message.date,
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
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_56(self):
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
                        'XXtextXX': getattr(message, 'text', None),
                        'content_type': message.content_type
                    }
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_57(self):
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
                        'TEXT': getattr(message, 'text', None),
                        'content_type': message.content_type
                    }
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_58(self):
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
                        'text': getattr(None, 'text', None),
                        'content_type': message.content_type
                    }
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_59(self):
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
                        'text': getattr(message, None, None),
                        'content_type': message.content_type
                    }
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_60(self):
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
                        'text': getattr('text', None),
                        'content_type': message.content_type
                    }
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_61(self):
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
                        'text': getattr(message, None),
                        'content_type': message.content_type
                    }
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_62(self):
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
                        'text': getattr(message, 'text', ),
                        'content_type': message.content_type
                    }
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_63(self):
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
                        'text': getattr(message, 'XXtextXX', None),
                        'content_type': message.content_type
                    }
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_64(self):
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
                        'text': getattr(message, 'TEXT', None),
                        'content_type': message.content_type
                    }
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_65(self):
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
                        'XXcontent_typeXX': message.content_type
                    }
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_66(self):
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
                        'CONTENT_TYPE': message.content_type
                    }
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_67(self):
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
                    
                    self.logger.info(None)
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_68(self):
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
                    
                    self.logger.info(f"Received update: {json.dumps(None, ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_69(self):
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
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=None, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_70(self):
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
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=None)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_71(self):
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
                    
                    self.logger.info(f"Received update: {json.dumps(ensure_ascii=False, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_72(self):
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
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_73(self):
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
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, )}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_74(self):
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
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=True, indent=2)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_75(self):
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
                    
                    self.logger.info(f"Received update: {json.dumps(update_data, ensure_ascii=False, indent=3)}")
                    
                    # Call the original handler
                    return await handler_func(message)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_76(self):
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
                    return await handler_func(None)
                
                # Register the wrapper with the bot
                return self.bot.message_handler(**kwargs)(wrapper)
            
            return decorator
        
        return logged_message_handler
    
    def xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_77(self):
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
                return self.bot.message_handler(**kwargs)(None)
            
            return decorator
        
        return logged_message_handler
    
    xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_1': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_1, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_2': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_2, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_3': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_3, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_4': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_4, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_5': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_5, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_6': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_6, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_7': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_7, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_8': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_8, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_9': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_9, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_10': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_10, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_11': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_11, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_12': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_12, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_13': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_13, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_14': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_14, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_15': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_15, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_16': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_16, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_17': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_17, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_18': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_18, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_19': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_19, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_20': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_20, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_21': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_21, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_22': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_22, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_23': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_23, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_24': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_24, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_25': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_25, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_26': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_26, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_27': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_27, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_28': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_28, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_29': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_29, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_30': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_30, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_31': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_31, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_32': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_32, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_33': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_33, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_34': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_34, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_35': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_35, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_36': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_36, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_37': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_37, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_38': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_38, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_39': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_39, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_40': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_40, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_41': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_41, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_42': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_42, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_43': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_43, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_44': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_44, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_45': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_45, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_46': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_46, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_47': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_47, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_48': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_48, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_49': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_49, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_50': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_50, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_51': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_51, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_52': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_52, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_53': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_53, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_54': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_54, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_55': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_55, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_56': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_56, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_57': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_57, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_58': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_58, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_59': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_59, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_60': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_60, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_61': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_61, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_62': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_62, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_63': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_63, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_64': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_64, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_65': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_65, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_66': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_66, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_67': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_67, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_68': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_68, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_69': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_69, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_70': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_70, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_71': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_71, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_72': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_72, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_73': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_73, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_74': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_74, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_75': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_75, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_76': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_76, 
        'xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_77': xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_77
    }
    
    def _create_logged_message_handler(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_orig"), object.__getattribute__(self, "xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _create_logged_message_handler.__signature__ = _mutmut_signature(xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_orig)
    xǁHandlerRegistryǁ_create_logged_message_handler__mutmut_orig.__name__ = 'xǁHandlerRegistryǁ_create_logged_message_handler'
    
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
                        username = message.from_user.username or message.from_user.first_name or "User"
                        await self.bot.reply_to(message, f"Welcome back, {username}")
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
    
    def xǁHandlerRegistryǁadd_custom_handler__mutmut_orig(self, decorator_kwargs, handler_func):
        """
        Utility method to add custom handlers dynamically
        
        Args:
            decorator_kwargs: Arguments for the logged_message_handler decorator
            handler_func: The async handler function
        """
        return self.logged_message_handler(**decorator_kwargs)(handler_func)
    
    def xǁHandlerRegistryǁadd_custom_handler__mutmut_1(self, decorator_kwargs, handler_func):
        """
        Utility method to add custom handlers dynamically
        
        Args:
            decorator_kwargs: Arguments for the logged_message_handler decorator
            handler_func: The async handler function
        """
        return self.logged_message_handler(**decorator_kwargs)(None)
    
    xǁHandlerRegistryǁadd_custom_handler__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHandlerRegistryǁadd_custom_handler__mutmut_1': xǁHandlerRegistryǁadd_custom_handler__mutmut_1
    }
    
    def add_custom_handler(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHandlerRegistryǁadd_custom_handler__mutmut_orig"), object.__getattribute__(self, "xǁHandlerRegistryǁadd_custom_handler__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_custom_handler.__signature__ = _mutmut_signature(xǁHandlerRegistryǁadd_custom_handler__mutmut_orig)
    xǁHandlerRegistryǁadd_custom_handler__mutmut_orig.__name__ = 'xǁHandlerRegistryǁadd_custom_handler'
