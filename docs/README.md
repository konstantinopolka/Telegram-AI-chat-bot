# Documentation

Welcome to the Telegram AI Chat Bot documentation! This folder contains comprehensive guides for working with the project.

## 📚 Documentation Index

### Getting Started

- **[Project README](../README.md)** - Main project documentation with quick start guide
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

## 🤝 Contributing to Documentation

When adding new documentation:

1. **Create a new .md file** in this folder
2. **Add it to this README** with description
3. **Link it from main README** if relevant
4. **Use clear headings** and table of contents
5. **Include code examples** where helpful
6. **Keep it up to date** with code changes

### Documentation Style Guide

- Use **clear, descriptive headings**
- Include **code examples** for complex topics
- Add **troubleshooting sections** for common issues
- Use **tables** for comparisons and references
- Include **diagrams** where helpful (Mermaid preferred)
- Keep **line length reasonable** (80-120 chars)
- Use **relative links** for internal references

## 📝 Feedback

Found an error in the documentation? Have a suggestion?

- Open an issue on GitHub
- Submit a pull request with improvements
- Ask questions in discussions

---

**Last Updated:** 2025-10-15
