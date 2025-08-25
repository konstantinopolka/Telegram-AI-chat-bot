# HandlerRegistry Pattern Implementation

## What is the HandlerRegistry Pattern?

The **HandlerRegistry** is a design pattern that separates the responsibility of **registering and organizing message handlers** from the main bot class. Think of it as a specialized "manager" that handles one specific job: organizing all the message handlers.

## Why Use HandlerRegistry?

### Before (Wrapper Functions):
```python
def register_welcome_handler(bot, logged_message_handler):
    @logged_message_handler(commands=['help', 'start'])
    async def send_welcome(message):
        await bot.reply_to(message, "Welcome!")

def register_all_handlers(bot, logged_message_handler):
    register_welcome_handler(bot, logged_message_handler)
    register_rules_handler(bot, logged_message_handler)
    register_echo_handler(bot, logged_message_handler)
```

### After (HandlerRegistry Class):
```python
class HandlerRegistry:
    def __init__(self, bot, logged_message_handler):
        self.bot = bot
        self.logged_message_handler = logged_message_handler
        self.register_all_handlers()
    
    def _register_welcome_handler(self):
        @self.logged_message_handler(commands=['help', 'start'])
        async def send_welcome(message):
            await self.bot.reply_to(message, "Welcome!")
```

## Key Benefits

### 1. **Clear Ownership**
- The `HandlerRegistry` **owns** all handler registration logic
- The `BotHandler` focuses on bot initialization and polling
- Clean separation of responsibilities

### 2. **Easy to Extend**
```python
# Adding a new handler is simple:
def _register_new_command_handler(self):
    @self.logged_message_handler(commands=['newcommand'])
    async def handle_new_command(message):
        await self.bot.reply_to(message, "New command!")
```

### 3. **Better Organization**
- All handlers are in one place
- Each handler has its own method
- Clear naming convention: `_register_*_handler()`

### 4. **Testability**
```python
# You can test the registry separately
registry = HandlerRegistry(mock_bot, mock_decorator)
# Test that handlers are registered correctly
```

### 5. **Dynamic Handler Management**
```python
# You can add handlers dynamically
registry.add_custom_handler(
    {'commands': ['dynamic']}, 
    some_handler_function
)
```

## How It Works

### 1. **BotHandler Creates the Registry**
```python
class BotHandler:
    def _register_handlers(self):
        logged_message_handler = create_logged_message_handler(self.bot, self.logger)
        # Create registry - it automatically registers all handlers
        self.handler_registry = HandlerRegistry(self.bot, logged_message_handler)
```

### 2. **Registry Registers All Handlers**
```python
class HandlerRegistry:
    def __init__(self, bot, logged_message_handler):
        self.bot = bot  # Store bot for handlers to use
        self.logged_message_handler = logged_message_handler  # Store decorator
        self.register_all_handlers()  # Register everything
```

### 3. **Handlers Use self.bot and self.logged_message_handler**
```python
def _register_echo_handler(self):
    @self.logged_message_handler(func=lambda message: True)
    async def echo_message(message):
        await self.bot.reply_to(message, f"You said: {message.text}")
        #     ^^^^^^^^ Uses self.bot from the registry
```

## Learning Points

This pattern teaches several OOP concepts:

1. **Single Responsibility Principle**: Each class has one job
2. **Composition**: BotHandler **uses** HandlerRegistry (has-a relationship)
3. **Encapsulation**: Handler logic is encapsulated in the registry
4. **Dependency Injection**: Bot and decorator are injected into the registry

## File Structure

```
src/
├── bot_handler/
│   └── bot_handler.py          # Main bot class (clean & focused)
├── handlers/
│   └── handler_registry.py     # Handler registration logic
├── utils/
│   └── logging_utils.py        # Logging utilities
└── dao/
    └── models.py              # Database models
```

This pattern makes the code more **organized**, **testable**, and **maintainable** while keeping each class focused on its specific responsibility!
