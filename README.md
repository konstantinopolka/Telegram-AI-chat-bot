# Telegram AI Chat Bot

A sophisticated Telegram bot for scraping articles, publishing to Telegraph, and managing content through a database-driven architecture.

## 📚 Complete Documentation

**All comprehensive documentation has been moved to the `docs/` folder.**

👉 **[Read the complete documentation here: docs/README.md](docs/README.md)**

## 🚀 Quick Start

```bash
# 1. Clone and navigate
git clone https://github.com/konstantinopolka/Telegram-AI-chat-bot.git
cd Telegram-AI-chat-bot

# 2. Set up environment
python -m venv venv
source venv/bin/activate  # On Linux/macOS

# 3. Install dependencies
pip install -r requirements/dev-requirements.txt

# 4. Configure .env file
# Add TELEGRAM_TOKEN, TELEGRAPH_ACCESS_TOKEN, DATABASE_URL

# 5. Create database
alembic upgrade head

# 6. Run the bot
python main.py
```

## 📖 Documentation Structure

- **[docs/README.md](docs/README.md)** - Complete project documentation (installation, usage, development)
- **[docs/database_guide.md](docs/database_guide.md)** - Database setup, models, and usage
- **[docs/auto_database_creation.md](docs/auto_database_creation.md)** - Automating database initialization
- **[docs/class_diagram.md](docs/class_diagram.md)** - System architecture diagram
- **[docs/telegraph_setup.md](docs/telegraph_setup.md)** - Telegraph configuration
- **[tests/README.md](tests/README.md)** - Testing guide
- **[docker/readme.md](docker/readme.md)** - Docker deployment guide

## ✨ Features

- Article scraping from review websites
- Telegraph integration with content splitting
- SQLModel database with Alembic migrations
- User management and tracking
- Channel posting capabilities
- Comprehensive logging
- Docker support
- Extensive testing

## 🤝 Contributing

See [docs/README.md](docs/README.md#-contributing) for contribution guidelines.

## 📜 License

Open source. Check repository for license details.

---

**For detailed information, see [docs/README.md](docs/README.md)**
