# Telegram AI Chat Bot - Complete Documentation

Welcome to the Telegram AI Chat Bot! This is a sophisticated bot built with **pyTelegramBotAPI (telebot)** that scrapes articles from review websites, publishes them to Telegraph, and manages content through a database-driven architecture.

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/konstantinopolka/Telegram-AI-chat-bot.git
cd Telegram-AI-chat-bot

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/macOS

# 3. Install dependencies
pip install -r requirements/dev-requirements.txt

# 4. Configure .env file (copy and edit)
# Add TELEGRAM_TOKEN, TELEGRAPH_ACCESS_TOKEN, DATABASE_URL

# 5. Create database
alembic upgrade head

# 6. Run the bot
python main.py
```

## ✨ Features

- **Article Scraping**: Automatically scrapes articles from review websites with configurable parsing
- **Telegraph Integration**: Publishes articles to Telegraph with automatic content splitting for large articles
- **Database Management**: SQLModel-based database with Alembic migrations for schema versioning
- **User Management**: Tracks users and their interactions with the bot
- **Channel Posting**: Posts articles to Telegram channels
- **Comprehensive Logging**: Logs all bot activity (incoming/outgoing) in JSON format
- **Modular Architecture**: Clean separation of concerns with abstract base classes for extensibility
- **Docker Support**: Production-ready Docker deployment with versioning
- **Extensive Testing**: Unit, integration, and system tests

## � Table of Contents

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture-overview)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Core Workflows](#-core-workflows)
- [Testing](#-testing)
- [Development](#-development)
- [Design Patterns](#-key-design-patterns)
- [Troubleshooting](#-troubleshooting)
- [Documentation Files](#-documentation-files)
- [Contributing](#-contributing)

## 📁 Project Structure

```text
Telegram-AI-chat-bot/
├── main.py                              # Application entry point
├── alembic.ini                          # Alembic configuration for migrations
├── pytest.ini                           # Pytest configuration
├── requirements.txt                     # Python dependencies
├── src/                                 # Source code
│   ├── bot_handler.py                   # Main bot controller
│   ├── handler_registry.py              # Message handler registration with logging
│   ├── telegraph_manager.py             # Telegraph article creation and management
│   ├── channel_poster.py                # Telegram channel posting
│   ├── reposting_orchestrator.py        # Orchestrates scraping → Telegraph → DB workflow
│   ├── version.py                       # Version information
│   ├── dao/                             # Data Access Layer
│   │   ├── models/                      # SQLModel database models
│   │   │   ├── user.py                  # User model
│   │   │   ├── article.py               # Article model
│   │   │   └── review.py                # Review model
│   │   ├── core/
│   │   │   └── database_manager.py      # Database connection management (Singleton)
│   │   ├── config/
│   │   │   └── database.py              # Database configuration
│   │   └── alembic/                     # Database migrations
│   │       ├── env.py                   # Alembic environment
│   │       └── versions/                # Migration scripts
│   └── scraping/                        # Web scraping modules
│       ├── scraper.py                   # Abstract scraper base class
│       ├── fetcher.py                   # Abstract HTTP fetcher base class
│       ├── parser.py                    # Abstract HTML parser base class
│       ├── review_scraper.py            # Concrete review scraper implementation
│       ├── review_fetcher.py            # Concrete HTTP fetcher for reviews
│       ├── review_parser.py             # Concrete HTML parser for reviews
│       └── constants.py                 # Scraping constants
├── tests/                               # Test suite
│   ├── unit/                            # Unit tests
│   ├── integration/                     # Integration tests
│   │   ├── scraping/                    # Scraping integration tests
│   │   └── system/                      # End-to-end system tests
│   ├── run_bulk_tests.sh               # Bulk test runner script
│   └── README.md                        # Testing documentation
├── docker/                              # Docker deployment
│   ├── Dockerfile                       # Multi-stage production build
│   ├── docker-compose.yml               # Service orchestration
│   ├── build.sh                         # Automated build with versioning
│   ├── deploy.sh                        # Registry deployment script
│   └── readme.md                        # Docker documentation
├── docs/                                # Documentation
│   ├── README.md                        # This file
│   ├── database_guide.md                # Complete database documentation
│   ├── auto_database_creation.md        # Database auto-creation guide
│   ├── class_diagram.md                 # Mermaid class diagram
│   └── telegraph_setup.md               # Telegraph setup guide
└── requirements/                        # Requirements by environment
    ├── base-requirements.txt            # Base dependencies
    ├── dev-requirements.txt             # Development dependencies
    └── prod-requirements.txt            # Production dependencies
```

## 🏗️ Architecture Overview

The bot follows a layered architecture with clear separation of concerns:

- **Bot Handler Layer**: `BotHandler` and `HandlerRegistry` manage Telegram interactions
- **Orchestration Layer**: `ReviewOrchestrator` coordinates the complete workflow
- **Scraping Layer**: Abstract base classes (`Scraper`, `Fetcher`, `Parser`) with concrete implementations for extensibility
- **Telegraph Layer**: `TelegraphManager` handles article publishing with automatic content splitting
- **Data Layer**: SQLModel models with Alembic migrations for schema management
- **Database Layer**: Singleton `DatabaseManager` for connection management

See [class_diagram.md](class_diagram.md) for a detailed Mermaid class diagram.

## 📦 Requirements

- Python 3.8+
- A Telegram bot token from [BotFather](https://t.me/BotFather)
- Telegraph account (for article publishing)
- SQLite or PostgreSQL database

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/konstantinopolka/Telegram-AI-chat-bot.git
cd Telegram-AI-chat-bot
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies

For development:

```bash
pip install -r requirements/dev-requirements.txt
```

For production:

```bash
pip install -r requirements/prod-requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Telegram Bot Configuration
TELEGRAM_TOKEN=your_telegram_bot_token_here

# Telegraph Configuration (for article publishing)
TELEGRAPH_ACCESS_TOKEN=your_telegraph_access_token_here
TELEGRAPH_SHORT_NAME=your_short_name
TELEGRAPH_AUTHOR_NAME=Your Author Name
TELEGRAPH_AUTHOR_URL=https://your-author-url.com/
TELEGRAPH_AUTH_URL=https://edit.telegra.ph/auth/your_auth_url_here

# Database Configuration
DATABASE_URL=sqlite:///dev.db
ASYNC_DATABASE_URL=sqlite+aiosqlite:///dev.db
# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/dbname
# ASYNC_DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
```

See [telegraph_setup.md](telegraph_setup.md) for detailed Telegraph setup instructions.

### 5. Initialize Database

**⚠️ IMPORTANT:** The database is NOT created automatically. You must create it using Alembic migrations.

Run this command from the project root:

```bash
alembic upgrade head
```

This will:

- Create the database file (`dev.db` for SQLite) or tables (for PostgreSQL)
- Create all tables: `reposting_bot_users`, `articles`, `reviews`
- Apply all schema migrations

**Documentation:**

- **[Database Guide](database_guide.md)** - Complete database documentation
- **[Auto Database Creation](auto_database_creation.md)** - Options for automatic database initialization

## 🚀 Usage

### Running the Bot Locally

Start the bot with async polling:

```bash
python main.py
```

The bot will:

- Start polling for Telegram messages
- Log all activity to console and `bot.log` file
- Display detailed JSON logs of incoming/outgoing messages
- Automatically handle user registration in the database

### Docker Deployment (Production)

Build and run with Docker:

```bash
cd docker
./build.sh                                      # Build with automatic versioning
docker-compose --env-file .env.docker up -d     # Start services
```

For detailed Docker setup, versioning system, and deployment to registries, see [../docker/readme.md](../docker/readme.md).

## 🔄 Core Workflows

### 1. Scraping and Publishing Articles

The `ReviewOrchestrator` manages the complete workflow:

```python
from src.reposting_orchestrator import ReviewOrchestrator
from src.scraping.review_scraper import ReviewScraper
from src.telegraph_manager import TelegraphManager

# Initialize components
scraper = ReviewScraper(base_url="https://example.com/review")
telegraph = TelegraphManager()

# Process entire review batch with explicit telegraph_manager for testability
orchestrator = ReviewOrchestrator(
    review_scraper=scraper,
    telegraph_manager=telegraph  # Optional: uses singleton if not provided
)

# Scrape → Telegraph → Database
review = await orchestrator.process_review_batch()
```

**Workflow Steps:**

1. **Scrape**: `ReviewScraper` fetches and parses articles from source website
2. **Publish**: `TelegraphManager` creates Telegraph articles (auto-splits if content is too large)
3. **Save**: Articles and reviews saved to database with SQLModel
4. **Post**: `ChannelPoster` shares articles to Telegram channel

### 2. User Interaction

Users interact with the bot through message handlers:

- `/start` or `/help` - Welcome message and user registration
- `/rules` - Bot rules
- Additional handlers can be added via `HandlerRegistry`

All interactions are logged in JSON format with full request/response details.

## 🧪 Testing

The project includes comprehensive test coverage:

### Run All Tests

```bash
# From project root
./tests/run_bulk_tests.sh
```

### Run Specific Test Suites

```bash
# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# Specific test file
pytest tests/unit/test_telegraph_manager.py

# With coverage
pytest --cov=src tests/
```

### Test Structure

- **Unit Tests** (`tests/unit/`): Test individual components in isolation
- **Integration Tests** (`tests/integration/`): Test component interactions
- **System Tests** (`tests/integration/system/`): End-to-end workflows

See [../tests/README.md](../tests/README.md) for detailed testing documentation.

## 💻 Development

### Adding New Message Handlers

Handlers are registered through `HandlerRegistry`. To add a new handler:

1. **Add to `HandlerRegistry`** in `src/handler_registry.py`:

```python
def _register_new_handler(self):
    """Register your new handler"""

    @self.logged_message_handler(commands=['weather'])
    async def weather_command(message):
        try:
            await self.bot.reply_to(message, "Today is sunny! ☀️")
        except Exception as e:
            self.logger.error(f"Error in weather_command: {e}", exc_info=True)
```

2. **Call registration method** in `register_all_handlers()`:

```python
def register_all_handlers(self):
    self._register_welcome_handler()
    self._register_rules_handler()
    self._register_new_handler()  # Add your handler
    self._register_echo_handler()  # Keep echo as last (catch-all)
```

All handlers automatically get logging via the `logged_message_handler` decorator.

### Adding New Scrapers

To scrape content from a different source:

1. **Create concrete implementations** of abstract base classes:

   - Extend `Fetcher` for HTTP operations
   - Extend `Parser` for HTML parsing
   - Extend `Scraper` for complete workflow

2. **Example structure**:

```python
from src.scraping import Fetcher, Parser, Scraper

class MyFetcher(Fetcher):
    def fetch_page(self, url: str) -> str:
        # Your implementation
        pass

class MyParser(Parser):
    def parse_listing_page(self, html: str) -> List[str]:
        # Your implementation
        pass

class MyScraper(Scraper):
    def __init__(self, base_url: str):
        self.fetcher = MyFetcher(base_url)
        self.parser = MyParser(base_url)
```

See `src/scraping/review_scraper.py` for a complete example.

### Database Migrations

When modifying database models, create a new Alembic migration:

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration in src/dao/alembic/versions/

# Apply the migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### Logging Configuration

Adjust logging level in `main.py`:

```python
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG, WARNING, or ERROR
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

## 🎨 Key Design Patterns

- **Singleton**: `DatabaseManager` and `TelegraphManager` ensure single instances with optional dependency injection
- **Abstract Factory**: Scraping module (`Scraper`, `Fetcher`, `Parser`) for extensibility
- **Decorator**: `HandlerRegistry` wraps handlers with automatic logging
- **Orchestrator**: `ReviewOrchestrator` coordinates complex multi-step workflows
- **Repository**: `DatabaseManager` abstracts database operations

## 🔧 Troubleshooting

### Bot doesn't respond

- Verify `TELEGRAM_TOKEN` in `.env` is correct
- Check console/`bot.log` for error messages
- Ensure no webhook is set (bot uses polling):

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/deleteWebhook"
```

### Database errors

- Ensure migrations are up to date: `alembic upgrade head`
- Check database URL in `.env`
- Verify database file permissions (for SQLite)

### Telegraph publishing fails

- Verify Telegraph credentials in `.env`
- Check [telegraph_setup.md](telegraph_setup.md) for setup instructions
- Ensure content doesn't contain disallowed HTML tags (see `src/scraping/constants.py`)

### Tests failing

- Install dev dependencies: `pip install -r requirements/dev-requirements.txt`
- Check test-specific configuration in `pytest.ini`
- Review test output for specific error details

## 📚 Documentation Files

### Getting Started

- **[Database Guide](database_guide.md)** - Complete guide to database setup, models, and usage

### Setup & Configuration

- **[Telegraph Setup](telegraph_setup.md)** - Configure Telegraph integration for article publishing
- **[Auto Database Creation](auto_database_creation.md)** - Options for automating database initialization

### Architecture & Design

- **[Class Diagram](class_diagram.md)** - Mermaid diagram showing complete system architecture

### Deployment

- **[Docker Guide](../docker/readme.md)** - Docker deployment with versioning system
- **[Testing Guide](../tests/README.md)** - Comprehensive testing documentation

## 🎯 Quick Navigation by Task

### I want to...

#### Set up the project for the first time

1. Read [Project README](../README.md) - Installation section
2. Follow [Database Guide](database_guide.md) - Setup sections
3. Configure [Telegraph Setup](telegraph_setup.md)
4. Run `alembic upgrade head`
5. Run `python main.py`

#### Understand the database

1. Read [Database Guide](database_guide.md) - Complete reference
2. Check models in `src/dao/models/`
3. Review migrations in `src/dao/alembic/versions/`

#### Make the database auto-create

1. Read [Auto Database Creation](auto_database_creation.md)
2. Choose your preferred approach (manual, auto-alembic, or Docker)
3. Implement the solution

#### Deploy to production

1. Read [Docker Guide](../docker/readme.md)
2. Set up Docker Compose with entrypoint script
3. Configure PostgreSQL database
4. Review [Database Guide](database_guide.md) - PostgreSQL section

#### Understand the architecture

1. Read [Class Diagram](class_diagram.md)
2. Review source code in `src/`
3. Check [Project README](../README.md) - Architecture section

#### Write tests

1. Read [Testing Guide](../tests/README.md)
2. Review existing tests in `tests/`
3. Run `./tests/run_bulk_tests.sh`

#### Add new features

1. Understand architecture from [Class Diagram](class_diagram.md)
2. Review [Project README](../README.md) - Development section
3. Add tests following [Testing Guide](../tests/README.md)
4. Create migration if needed (see [Database Guide](database_guide.md))

## 📖 Documentation Files

### [database_guide.md](database_guide.md)

**Comprehensive database documentation** covering:

- Database structure and ERD
- SQLModel models (User, Article, Review)
- Setup for SQLite and PostgreSQL
- Using database in code (async sessions)
- Creating and applying migrations
- Complex queries and relationships
- FAQ with common issues and solutions

**Read this if:** You need to work with the database, create migrations, or understand data models.

### [auto_database_creation.md](auto_database_creation.md)

**Guide to automating database initialization** covering:

- Why database isn't auto-created by default
- Solution 1: Manual (recommended for dev)
- Solution 2: Auto-create on startup (simple)
- Solution 3: Auto-run Alembic (better)
- Solution 4: Docker entrypoint (production)
- Implementation examples
- Testing auto-creation

**Read this if:** You want the database to be created automatically when running the bot.

### [telegraph_setup.md](telegraph_setup.md)

**Telegraph integration configuration** covering:

- Environment variable setup
- Obtaining Telegraph credentials
- Testing Telegraph connection
- Troubleshooting common issues

**Read this if:** You need to set up or troubleshoot Telegraph article publishing.

### [class_diagram.md](class_diagram.md)

**Complete system architecture visualization** covering:

- Mermaid class diagram of entire codebase
- Component descriptions
- Relationships between classes
- Design patterns used
- Data flow diagrams

**Read this if:** You want to understand the big picture architecture or navigate the codebase.

## 🔗 External Documentation

### Dependencies

- **[SQLModel](https://sqlmodel.tiangolo.com/)** - Database ORM (SQLAlchemy + Pydantic)
- **[Alembic](https://alembic.sqlalchemy.org/)** - Database migrations
- **[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)** - Telegram Bot API wrapper
- **[Telegraph API](https://telegra.ph/api)** - Telegraph publishing API
- **[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)** - HTML parsing
- **[pytest](https://docs.pytest.org/)** - Testing framework

### Related Resources

- **[Telegram Bot API](https://core.telegram.org/bots/api)** - Official Telegram Bot documentation
- **[SQLAlchemy](https://docs.sqlalchemy.org/)** - Advanced ORM features
- **[Docker](https://docs.docker.com/)** - Container deployment
- **[PostgreSQL](https://www.postgresql.org/docs/)** - Production database

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and add tests
4. Run test suite: `./tests/run_bulk_tests.sh`
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature/your-feature`
7. Create Pull Request

### Contributing to Documentation

When adding new documentation:

1. **Create a new .md file** in the `docs/` folder
2. **Add it to this README** with description
3. **Use clear headings** and table of contents
4. **Include code examples** where helpful
5. **Keep it up to date** with code changes

### Documentation Style Guide

- Use **clear, descriptive headings**
- Include **code examples** for complex topics
- Add **troubleshooting sections** for common issues
- Use **tables** for comparisons and references
- Include **diagrams** where helpful (Mermaid preferred)
- Keep **line length reasonable** (80-120 chars)
- Use **relative links** for internal references

## 📜 License

This project is open source. Please check the repository for license details.

## 🔐 Security Note

**Keep `.env` file and all tokens secure.** Never commit secrets to version control. Use `.gitignore` to exclude sensitive files.

## 📞 Support

Found an error in the documentation? Have a suggestion?

- Open an issue on GitHub
- Submit a pull request with improvements
- Ask questions in discussions

## 🔗 External Resources

### Dependencies Documentation

- [SQLModel](https://sqlmodel.tiangolo.com/) - Database ORM (SQLAlchemy + Pydantic)
- [Alembic](https://alembic.sqlalchemy.org/) - Database migrations
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) - Telegram Bot API wrapper
- [Telegraph API](https://telegra.ph/api) - Telegraph publishing API
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - HTML parsing
- [pytest](https://docs.pytest.org/) - Testing framework

### Related Resources

- [Telegram Bot API](https://core.telegram.org/bots/api) - Official Telegram Bot documentation
- [SQLAlchemy](https://docs.sqlalchemy.org/) - Advanced ORM features
- [Docker](https://docs.docker.com/) - Container deployment
- [PostgreSQL](https://www.postgresql.org/docs/) - Production database

---

**Last Updated:** 2025-10-15  
**Repository:** [konstantinopolka/Telegram-AI-chat-bot](https://github.com/konstantinopolka/Telegram-AI-chat-bot)
