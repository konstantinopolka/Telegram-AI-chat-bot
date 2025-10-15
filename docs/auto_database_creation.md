# Auto-Creating Database on Startup

This document explains how to automatically create the database when it doesn't exist.

## The Problem

When you clone the repository and run the code, you get errors like:

```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: reposting_bot_users
```

This happens because **the database is not created automatically by the code**. This is intentional for production safety and schema version control.

## Why Not Auto-Create by Default?

### Reasons for Manual Initialization

1. **Version Control**: Using Alembic migrations ensures:

   - Schema changes are tracked
   - All environments have the same schema version
   - You can rollback changes if needed

2. **Production Safety**:

   - Prevents accidental schema changes
   - Makes it explicit when database setup happens
   - Avoids data loss from unexpected schema modifications

3. **Team Collaboration**:
   - Everyone knows the exact database version
   - Migration history is visible in git
   - Easier to debug schema-related issues

## Solution 1: Manual (Recommended for Development)

Simply run before starting the bot:

```bash
alembic upgrade head
```

**Pros:**

- Full control over when database is created
- Uses proper migrations
- Best practice for development

**Cons:**

- Extra step to remember

## Solution 2: Auto-Create on Startup (Simple)

Add this to `main.py`:

```python
import os
import logging
from src.dao.core.database_manager import DatabaseManager

logger = logging.getLogger(__name__)

async def ensure_database_exists():
    """Create database tables if they don't exist"""
    db_manager = DatabaseManager()

    # For SQLite: Check if database file exists
    db_url = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    if db_url.startswith("sqlite"):
        db_file = db_url.replace("sqlite:///", "")
        if not os.path.exists(db_file):
            logger.info("Database not found. Creating tables...")
            await db_manager.create_all_tables()
            logger.info("Database created successfully!")
            return

    # For PostgreSQL: Try to connect, create if connection fails
    try:
        async with db_manager.get_async_session() as session:
            # Try a simple query to check if tables exist
            from sqlmodel import text
            result = await session.execute(text("SELECT 1 FROM reposting_bot_users LIMIT 1"))
            logger.info("Database tables already exist")
    except Exception as e:
        logger.info(f"Database tables don't exist. Creating... ({e})")
        await db_manager.create_all_tables()
        logger.info("Database created successfully!")

async def main():
    """Main function with proper exception handling"""
    try:
        logger.info("Starting bot...")

        # Ensure database exists before starting bot
        await ensure_database_exists()

        bot_handler = BotHandler()
        await bot_handler.start_polling()

    except Exception as e:
        logger.error(f"Critical error in bot polling: {e}", exc_info=True)
        raise
    finally:
        logger.info("Bot stopped")
```

**Pros:**

- No extra commands needed
- Works for first-time setup
- Simple to implement

**Cons:**

- Bypasses Alembic migrations (doesn't use version control)
- If you update models, you still need to run migrations manually
- Not recommended for production

## Solution 3: Auto-Run Alembic on Startup (Better)

Add this to `main.py`:

```python
import subprocess
import logging

logger = logging.getLogger(__name__)

def run_migrations():
    """Run Alembic migrations before starting bot"""
    try:
        logger.info("Running database migrations...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))  # Run from project root
        )
        logger.info(f"Migrations completed: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error("Alembic command not found. Please install alembic: pip install alembic")
        return False

async def main():
    """Main function with proper exception handling"""
    try:
        logger.info("Starting bot...")

        # Run migrations automatically
        if not run_migrations():
            logger.error("Failed to run migrations. Exiting.")
            sys.exit(1)

        bot_handler = BotHandler()
        await bot_handler.start_polling()

    except Exception as e:
        logger.error(f"Critical error in bot polling: {e}", exc_info=True)
        raise
    finally:
        logger.info("Bot stopped")
```

**Pros:**

- Uses proper Alembic migrations
- Schema version is tracked
- Works for both SQLite and PostgreSQL
- Automatically applies new migrations

**Cons:**

- Requires `alembic` command in PATH
- Slightly slower startup (runs migrations check)
- May not work in some restricted environments

## Solution 4: Docker Entrypoint (Best for Production)

Modify `docker/docker-compose.yml`:

```yaml
version: "3.8"

services:
  bot:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: telegram-bot
    restart: unless-stopped
    env_file:
      - .env.docker
    entrypoint: ["/bin/sh", "-c"]
    command:
      - |
        echo "Running database migrations..."
        alembic upgrade head
        echo "Starting bot..."
        python main.py
    volumes:
      - bot-data:/app/data
    networks:
      - bot-network

volumes:
  bot-data:

networks:
  bot-network:
```

Or modify `docker/Dockerfile` to include an entrypoint script:

```dockerfile
# Add to Dockerfile
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

Create `docker/entrypoint.sh`:

```bash
#!/bin/sh
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"
```

**Pros:**

- Industry standard approach
- Works with container orchestration (Kubernetes, Docker Swarm)
- Always runs migrations before starting
- Production-ready

**Cons:**

- Only works with Docker deployment
- Requires understanding of Docker

## Recommended Approach by Environment

### Development (Local)

**Option:** Manual migrations before running

```bash
alembic upgrade head
python main.py
```

### Development (Automated)

**Option:** Solution 3 (Auto-run Alembic)

Add migration auto-run to `main.py`

### Production (Docker)

**Option:** Solution 4 (Docker Entrypoint)

Run migrations in container entrypoint

### Production (Bare Metal)

**Option:** Systemd service with pre-start script

```ini
# /etc/systemd/system/telegram-bot.service
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=bot
WorkingDirectory=/opt/telegram-bot
ExecStartPre=/opt/telegram-bot/venv/bin/alembic upgrade head
ExecStart=/opt/telegram-bot/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Implementation Example

Here's a complete `main.py` with auto-migration:

```python
#!/usr/bin/python

import asyncio
import logging
import sys
import os
import subprocess
from dotenv import load_dotenv
from src.bot_handler import BotHandler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run Alembic migrations before starting bot"""
    try:
        logger.info("Checking database migrations...")
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            logger.info(f"Migration output: {result.stdout}")
        logger.info("Database is up to date")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e.stderr}")
        return False
    except FileNotFoundError:
        logger.error("Alembic not found. Please install: pip install alembic")
        return False

async def main():
    """Main function with proper exception handling"""
    try:
        logger.info("Starting Telegram AI Chat Bot...")

        # Run migrations automatically
        if not run_migrations():
            logger.error("Failed to initialize database. Exiting.")
            sys.exit(1)

        # Start bot
        bot_handler = BotHandler()
        await bot_handler.start_polling()

    except Exception as e:
        logger.error(f"Critical error in bot polling: {e}", exc_info=True)
        raise
    finally:
        logger.info("Bot stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
```

## Testing Auto-Creation

### Test with SQLite

```bash
# Remove existing database
rm dev.db

# Run bot (should auto-create)
python main.py

# Verify database was created
ls -la dev.db
sqlite3 dev.db ".tables"
```

### Test with PostgreSQL

```bash
# Drop database
psql -U postgres -c "DROP DATABASE IF EXISTS telegram_bot_db;"
psql -U postgres -c "CREATE DATABASE telegram_bot_db;"

# Run bot (should auto-create tables)
python main.py

# Verify tables were created
psql -U bot_user -d telegram_bot_db -c "\dt"
```

## Summary

| Solution          | Effort | Safety | Flexibility | Recommendation                 |
| ----------------- | ------ | ------ | ----------- | ------------------------------ |
| Manual            | Low    | High   | High        | ⭐ Development                 |
| Auto-Create       | Low    | Low    | Low         | ❌ Not recommended             |
| Auto-Alembic      | Medium | High   | High        | ⭐ Development with automation |
| Docker Entrypoint | Medium | High   | High        | ⭐ Production                  |

**Best practice:** Use Solution 3 (Auto-run Alembic) for development and Solution 4 (Docker Entrypoint) for production.
