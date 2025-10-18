# Copilot Instructions for Telegram-AI-chat-bot

## Project Overview

- **Purpose:** Telegram bot for echoing messages, handling commands, and posting to Telegraph.
- **Main entrypoint:** `main.py` (starts bot, sets up handlers)
- **Core logic:** Located in `src/` (bot logic, handlers, data access, scraping)
- **Database:** Uses Alembic migrations in `src/dao/alembic/` for schema management.
- **External services:** Integrates with Telegram API and Telegraph API (see `.env` for required tokens).

## Architecture & Patterns

- **Handlers:** Modular, each command/feature in its own file (see `src/handlers/` and `src/bot_handler.py`).
- **Logging:** Centralized logging via `src/logging_config.py`. All modules use `get_logger(__name__)`. Logs to both console and rotating file (`logs/bot.log`). Configure via environment variables (`LOG_LEVEL`, `LOG_FILE`, etc.).
- **Error handling:** Exceptions are logged with stack traces using `logger.error(..., exc_info=True)`; fallback messages are sent to users.
- **Scraping:** Logic for fetching/parsing reviews and articles is in `src/scraping/`.
- **Database access:** Models in `src/dao/models/`, migrations in `src/dao/alembic/`, DatabaseManager (singleton) in `src/dao/core/database_manager.py`.

## Developer Workflows

- **Run locally:** `python main.py`
- **Run tests:**
  - All tests: `tests/run_bulk_tests.sh`
  - Single test: `pytest tests/unit/test_telegraph_manager.py` (or other test file)
- **Docker:**
  - Build: `docker/build.sh`
  - Deploy: `docker/deploy.sh`
  - Compose: `docker/docker-compose.yml`
- **Migrations:**
  - Alembic migration scripts in `src/dao/alembic/versions/`

## Conventions & Tips

- **Environment:** All secrets/tokens in `.env` (never commit).
- **Handler registration:** Add new handlers to `src/handler_registry.py` and import in `main.py`.
- **Logging:** Use `from src.logging_config import get_logger; logger = get_logger(__name__)` in every module. Set level via `LOG_LEVEL` env var (default: INFO).
- **Testing:** Unit tests in `tests/unit/`, integration in `tests/integration/`, system in `tests/integration/system/`.
- **Scraping:** Use `src/scraping/review_scraper.py` for review-related scraping.

## Integration Points

- **Telegram:** All bot interactions via Telegram API (see `src/bot_handler.py`).
- **Telegraph:** Article/review posting via `src/telegraph_manager.py`.
- **Database:** SQLModel-based models, Alembic migrations.

## Examples

- **Add handler:**
  ```python
  # src/handlers/weather.py
  from src/bot_instance import bot
  @bot.message_handler(commands=['weather'])
  async def weather_command(message):
      await bot.reply_to(message, "Today is sunny! ☀️")
  ```
- **Run all tests:**
  ```bash
  ./tests/run_bulk_tests.sh
  ```
- **Build Docker image:**
  ```bash
  cd docker && ./build.sh
  ```

---

For more details, see `README.md`, `docker/readme.md`, and source files in `src/`.
