# Database Guide

This guide explains everything about the database layer in the Telegram AI Chat Bot project.

## Table of Contents

1. [Overview](#overview)
2. [Database Structure](#database-structure)
3. [Models](#models)
4. [Database Setup](#database-setup)
5. [Using the Database in Code](#using-the-database-in-code)
6. [Migrations](#migrations)
7. [Database Managers](#database-managers)
8. [FAQ](#faq)

## Overview

The project uses **SQLModel** (built on SQLAlchemy and Pydantic) for database operations with **Alembic** for schema migrations.

### Key Components

```
src/dao/
├── models/              # Database models (tables)
│   ├── user.py          # User model
│   ├── article.py       # Article model
│   └── review.py        # Review model
├── core/
│   └── database_manager.py  # Database connection manager (Singleton)
├── config/
│   └── database.py      # Database configuration and URLs
└── alembic/             # Database migrations
    ├── env.py           # Alembic environment
    └── versions/        # Migration scripts
```

### Supported Databases

- **SQLite** - For development, testing, and small deployments
- **PostgreSQL** - For production deployments

## Database Structure

### Entity Relationship Diagram

```
┌─────────────────────┐
│   User              │
│─────────────────────│
│ telegram_id (PK)    │
│ username            │
│ first_name          │
│ last_name           │
│ phone               │
│ is_admin            │
│ registered_at       │
└─────────────────────┘

┌─────────────────────┐         ┌─────────────────────┐
│   Review            │         │   Article           │
│─────────────────────│         │─────────────────────│
│ id (PK)             │────1:N──│ id (PK)             │
│ source_url          │         │ title               │
│ created_at          │         │ content             │
│                     │         │ original_url        │
│                     │         │ review_id (FK)      │
│                     │         │ telegraph_urls      │
│                     │         │ authors             │
│                     │         │ created_at          │
└─────────────────────┘         └─────────────────────┘
```

### Tables

#### `reposting_bot_users`

Stores Telegram user information.

| Column        | Type        | Description                 |
| ------------- | ----------- | --------------------------- |
| telegram_id   | BIGINT (PK) | Telegram user ID            |
| username      | VARCHAR(50) | Telegram username           |
| first_name    | VARCHAR(50) | User's first name           |
| last_name     | VARCHAR(50) | User's last name (nullable) |
| phone         | VARCHAR(20) | Phone number (nullable)     |
| is_admin      | BOOLEAN     | Admin flag (default: true)  |
| registered_at | TIMESTAMP   | Registration timestamp      |

#### `reviews`

Stores review metadata (collection of articles).

| Column     | Type         | Description         |
| ---------- | ------------ | ------------------- |
| id         | INTEGER (PK) | Auto-increment ID   |
| source_url | VARCHAR(500) | Original review URL |
| created_at | TIMESTAMP    | Creation timestamp  |

#### `articles`

Stores individual articles scraped from reviews.

| Column         | Type         | Description               |
| -------------- | ------------ | ------------------------- |
| id             | INTEGER (PK) | Auto-increment ID         |
| title          | VARCHAR(255) | Article title             |
| content        | TEXT         | Article HTML content      |
| original_url   | VARCHAR(500) | Original article URL      |
| review_id      | INTEGER (FK) | Foreign key to reviews.id |
| telegraph_urls | JSON         | List of Telegraph URLs    |
| authors        | JSON         | List of author names      |
| created_at     | TIMESTAMP    | Creation timestamp        |

## Models

All models are defined in `src/dao/models/` using SQLModel.

### User Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class User(SQLModel, table=True):
    __tablename__ = "reposting_bot_users"

    telegram_id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=50)
    first_name: str = Field(max_length=50)
    last_name: Optional[str] = Field(max_length=50)
    phone: Optional[str] = Field(max_length=20)
    is_admin: bool = Field(default=True)
    registered_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
```

### Review Model

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: Optional[int] = Field(default=None, primary_key=True)
    source_url: str = Field(max_length=500)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    # Relationship: one review -> many articles
    articles: Optional[List["Article"]] = Relationship(back_populates="review")
```

### Article Model

```python
from sqlmodel import SQLModel, Field, Relationship, JSON
from typing import Optional, List

class Article(SQLModel, table=True):
    __tablename__ = "articles"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    content: str
    original_url: str = Field(max_length=500)
    review_id: int = Field(foreign_key="reviews.id")
    telegraph_urls: Optional[List[str]] = Field(default_factory=list, sa_type=JSON)
    authors: Optional[List[str]] = Field(default_factory=list, sa_type=JSON)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    # Relationship: many articles -> one review
    review: Optional["Review"] = Relationship(back_populates="articles")
```

## Database Setup

### ⚠️ Important: Database is NOT Created Automatically

When you clone the repository, **no database exists**. You must create it manually using Alembic migrations.

### Setup for SQLite (Development)

#### 1. Configure `.env`

```env
DATABASE_URL=sqlite:///dev.db
ASYNC_DATABASE_URL=sqlite+aiosqlite:///dev.db
```

#### 2. Create Database and Tables

From the project root:

```bash
alembic upgrade head
```

This will:

- Create `dev.db` file in the project root
- Create all tables (`reposting_bot_users`, `articles`, `reviews`)
- Apply all migrations

#### 3. Verify Database

```bash
# Check current migration version
alembic current

# View database (optional)
sqlite3 dev.db
sqlite> .tables
sqlite> .schema reposting_bot_users
sqlite> .quit
```

### Setup for PostgreSQL (Production)

#### 1. Install PostgreSQL

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
```

#### 2. Create Database

```bash
# Login as postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE telegram_bot_db;
CREATE USER bot_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE telegram_bot_db TO bot_user;
\q
```

#### 3. Configure `.env`

```env
DATABASE_URL=postgresql://bot_user:your_secure_password@localhost/telegram_bot_db
ASYNC_DATABASE_URL=postgresql+asyncpg://bot_user:your_secure_password@localhost/telegram_bot_db
```

#### 4. Create Tables

```bash
alembic upgrade head
```

#### 5. Verify Database

```bash
psql -U bot_user -d telegram_bot_db
\dt
\d reposting_bot_users
\q
```

## Using the Database in Code

### Async Session (Recommended)

Use `AsyncSessionLocal` for async operations (required for bot handlers):

```python
from src.dao import AsyncSessionLocal
from src.dao.models import User, Article, Review

async def save_user(telegram_id: int, username: str, first_name: str):
    """Save a new user to the database"""
    async with AsyncSessionLocal() as session:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

async def get_user(telegram_id: int):
    """Retrieve a user from the database"""
    async with AsyncSessionLocal() as session:
        user = await session.get(User, telegram_id)
        return user

async def get_all_articles():
    """Get all articles with their reviews"""
    from sqlmodel import select

    async with AsyncSessionLocal() as session:
        statement = select(Article)
        results = await session.execute(statement)
        articles = results.scalars().all()
        return articles

async def get_review_with_articles(review_id: int):
    """Get a review with all its articles (using relationship)"""
    from sqlmodel import select

    async with AsyncSessionLocal() as session:
        statement = select(Review).where(Review.id == review_id)
        result = await session.execute(statement)
        review = result.scalar_one_or_none()

        if review:
            # Access related articles through relationship
            # Note: May need to eagerly load with selectinload
            print(f"Review has {len(review.articles)} articles")

        return review
```

### Using in Bot Handlers

Example from `HandlerRegistry`:

```python
@self.logged_message_handler(commands=['help', 'start'])
async def send_welcome(message):
    try:
        async with AsyncSessionLocal() as session:
            # Check if user exists
            user = await session.get(User, message.from_user.id)

            if not user:
                # Create new user
                user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name
                )
                session.add(user)
                await session.commit()

                await self.bot.reply_to(message, "Welcome! You've been registered.")
            else:
                await self.bot.reply_to(message, f"Welcome back, {user.first_name}!")

    except Exception as e:
        self.logger.error(f"Error in send_welcome: {e}", exc_info=True)
```

### Using in Orchestrator

Example from `RepostingOrchestrator`:

```python
async def process_single_article(self, article: Article) -> Article:
    """Process and save article"""
    try:
        # Create Telegraph article
        telegraph_urls = await self.telegraph.create_article(article)

        if telegraph_urls:
            # Update article with Telegraph URLs
            article.telegraph_urls = telegraph_urls

            # Save to database
            async with self.db() as session:  # self.db is AsyncSessionLocal
                session.add(article)
                await session.commit()
                await session.refresh(article)

            print(f"Successfully processed article: {article.title}")
            return article

    except Exception as e:
        print(f"Error processing article: {e}")
        return None
```

### Complex Queries

```python
from sqlmodel import select
from src.dao import AsyncSessionLocal
from src.dao.models import Article, Review

async def get_recent_articles(limit: int = 10):
    """Get most recent articles"""
    async with AsyncSessionLocal() as session:
        statement = (
            select(Article)
            .order_by(Article.created_at.desc())
            .limit(limit)
        )
        results = await session.execute(statement)
        return results.scalars().all()

async def search_articles_by_author(author_name: str):
    """Search articles by author name (JSON array contains)"""
    async with AsyncSessionLocal() as session:
        statement = select(Article).where(
            Article.authors.contains([author_name])
        )
        results = await session.execute(statement)
        return results.scalars().all()

async def get_articles_by_review_url(review_url: str):
    """Get all articles from a specific review"""
    async with AsyncSessionLocal() as session:
        statement = (
            select(Article)
            .join(Review)
            .where(Review.source_url == review_url)
        )
        results = await session.execute(statement)
        return results.scalars().all()
```

## Migrations

### Understanding Migrations

Migrations are version-controlled changes to your database schema. Each migration is a Python script in `src/dao/alembic/versions/`.

### Creating a Migration

#### 1. Modify Your Model

Edit a model in `src/dao/models/`:

```python
# Add a new field to User model
class User(SQLModel, table=True):
    __tablename__ = "reposting_bot_users"

    telegram_id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=50)
    first_name: str = Field(max_length=50)
    last_name: Optional[str] = Field(max_length=50)
    phone: Optional[str] = Field(max_length=20)
    is_admin: bool = Field(default=True)
    registered_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))

    # NEW FIELD
    language: Optional[str] = Field(max_length=10, default="en")
```

#### 2. Generate Migration

```bash
alembic revision --autogenerate -m "Add language field to User"
```

This creates a new file in `src/dao/alembic/versions/` like `abc123def456_add_language_field_to_user.py`.

#### 3. Review the Migration

Open the generated file and verify the changes:

```python
def upgrade() -> None:
    # ### commands auto generated by Alembic ###
    op.add_column('reposting_bot_users', sa.Column('language', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic ###
    op.drop_column('reposting_bot_users', 'language')
    # ### end Alembic commands ###
```

#### 4. Apply the Migration

```bash
alembic upgrade head
```

### Migration Commands

```bash
# Check current database version
alembic current

# View migration history
alembic history

# View pending migrations
alembic history --verbose

# Upgrade to latest
alembic upgrade head

# Upgrade by 1 version
alembic upgrade +1

# Downgrade by 1 version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade abc123def456

# View SQL without applying
alembic upgrade head --sql
```

## Database Managers

### DatabaseManager (Singleton)

Located in `src/dao/core/database_manager.py`, this class manages database connections.

```python
from src.dao.core.database_manager import DatabaseManager

# Get instance (singleton pattern)
db_manager = DatabaseManager()

# Get async session
async with db_manager.get_async_session() as session:
    # Use session
    pass

# Create all tables (alternative to Alembic)
await db_manager.create_all_tables()

# Drop all tables (BE CAREFUL!)
await db_manager.drop_all_tables()
```

### Importing Sessions Directly

Preferred method for most use cases:

```python
from src.dao import AsyncSessionLocal

async with AsyncSessionLocal() as session:
    # Your database operations
    pass
```

## FAQ

### Why doesn't the database get created automatically when I run the code?

**Short Answer:** This is by design for safety and control.

**Detailed Explanation:**

1. **Schema Versioning**: Using Alembic migrations ensures:

   - All schema changes are tracked
   - Database state is consistent across environments
   - You can rollback changes if needed
   - Team members have the same schema version

2. **Production Safety**: Automatic database creation could:

   - Create schemas with wrong permissions
   - Cause data loss if schema changes unexpectedly
   - Make it unclear what version of the schema is running

3. **Best Practice**: Explicit initialization (`alembic upgrade head`) makes it clear when the database is being set up.

### Can I automate database creation?

**Yes**, you have several options:

#### Option 1: Check and Create on Startup (Simple)

Add to `main.py`:

```python
import os
from src.dao.core.database_manager import DatabaseManager

async def ensure_database_exists():
    """Create database tables if they don't exist"""
    db_manager = DatabaseManager()

    # Check if database file exists (SQLite only)
    db_url = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    if db_url.startswith("sqlite"):
        db_file = db_url.replace("sqlite:///", "")
        if not os.path.exists(db_file):
            logger.info("Database not found. Creating tables...")
            await db_manager.create_all_tables()
            logger.info("Database created successfully!")

async def main():
    try:
        logger.info("Starting bot...")

        # Ensure database exists
        await ensure_database_exists()

        bot_handler = BotHandler()
        await bot_handler.start_polling()

    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
        raise
```

**Limitations:**

- Bypasses Alembic migrations
- All migrations must be applied manually later
- Not recommended for production

#### Option 2: Run Alembic Programmatically

Add to `main.py`:

```python
import subprocess
import os

def run_migrations():
    """Run Alembic migrations before starting bot"""
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"Migrations applied: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e.stderr}")
        raise

async def main():
    try:
        logger.info("Starting bot...")

        # Run migrations automatically
        run_migrations()

        bot_handler = BotHandler()
        await bot_handler.start_polling()

    except Exception as e:
        logger.error(f"Critical error: {e}", exc_info=True)
        raise
```

**Advantages:**

- Uses Alembic migrations properly
- Works for any database (SQLite, PostgreSQL)
- Keeps schema versioning

**Limitations:**

- Requires `alembic` command in PATH
- May not work in some deployment environments

#### Option 3: Docker Entrypoint (Recommended for Production)

In `docker/docker-compose.yml`:

```yaml
services:
  bot:
    image: telegram-bot:latest
    entrypoint: ["/bin/sh", "-c"]
    command:
      - |
        alembic upgrade head
        python main.py
    environment:
      - DATABASE_URL=${DATABASE_URL}
```

**Advantages:**

- Best for production
- Always runs migrations before starting
- Works with orchestration tools (Kubernetes, Docker Swarm)

### How do I backup my database?

#### SQLite

```bash
# Simple copy
cp dev.db dev.db.backup

# With timestamp
cp dev.db "dev.db.backup.$(date +%Y%m%d_%H%M%S)"

# Restore
cp dev.db.backup dev.db
```

#### PostgreSQL

```bash
# Backup
pg_dump -U bot_user telegram_bot_db > backup.sql

# Backup with timestamp
pg_dump -U bot_user telegram_bot_db > "backup_$(date +%Y%m%d_%H%M%S).sql"

# Restore
psql -U bot_user telegram_bot_db < backup.sql
```

### How do I reset my database?

#### SQLite

```bash
# Delete database file
rm dev.db

# Recreate with migrations
alembic upgrade head
```

#### PostgreSQL

```bash
# Drop and recreate database
psql -U postgres
DROP DATABASE telegram_bot_db;
CREATE DATABASE telegram_bot_db;
GRANT ALL PRIVILEGES ON DATABASE telegram_bot_db TO bot_user;
\q

# Recreate tables
alembic upgrade head
```

### How do I switch from SQLite to PostgreSQL?

1. **Setup PostgreSQL** (see [Setup for PostgreSQL](#setup-for-postgresql-production))

2. **Update `.env`**:

```env
DATABASE_URL=postgresql://bot_user:password@localhost/telegram_bot_db
ASYNC_DATABASE_URL=postgresql+asyncpg://bot_user:password@localhost/telegram_bot_db
```

3. **Run migrations on new database**:

```bash
alembic upgrade head
```

4. **Migrate data** (if needed):

```bash
# Export from SQLite
sqlite3 dev.db .dump > data_export.sql

# Import to PostgreSQL (may need manual adjustments)
# This is complex - consider writing a Python script
```

### How do I view my data?

#### SQLite

```bash
# Open database
sqlite3 dev.db

# Common commands
.tables                          # List tables
.schema reposting_bot_users      # Show table structure
SELECT * FROM reposting_bot_users; # Query data
.quit                            # Exit
```

#### PostgreSQL

```bash
# Open database
psql -U bot_user -d telegram_bot_db

# Common commands
\dt                              -- List tables
\d reposting_bot_users          -- Show table structure
SELECT * FROM reposting_bot_users; -- Query data
\q                               -- Exit
```

#### Python Script

```python
import asyncio
from src.dao import AsyncSessionLocal
from src.dao.models import User, Article, Review
from sqlmodel import select

async def view_all_data():
    async with AsyncSessionLocal() as session:
        # View users
        users = (await session.execute(select(User))).scalars().all()
        print(f"Users: {len(users)}")
        for user in users:
            print(f"  {user.telegram_id}: {user.username}")

        # View reviews
        reviews = (await session.execute(select(Review))).scalars().all()
        print(f"\nReviews: {len(reviews)}")
        for review in reviews:
            print(f"  {review.id}: {review.source_url}")

        # View articles
        articles = (await session.execute(select(Article))).scalars().all()
        print(f"\nArticles: {len(articles)}")
        for article in articles:
            print(f"  {article.id}: {article.title}")

if __name__ == "__main__":
    asyncio.run(view_all_data())
```

## Additional Resources

- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
