"""
Data Access Layer

Provides:
- DatabaseManager (singleton)
- Repositories for each model
- Models
"""

from src.dao.core.database_manager import db_manager, DatabaseManager
from src.dao.repositories.user_repository import user_repository, UserRepository
from src.dao.repositories.article_repository import article_repository, ArticleRepository
from src.dao.repositories.review_repository import review_repository, ReviewRepository

__all__ = [
    # Database Manager
    "db_manager",
    "DatabaseManager",
    
    # Repositories (singleton instances)
    "user_repository",
    "article_repository",
    "review_repository",
    
    # Repository classes (for custom instantiation if needed)
    "UserRepository",
    "ArticleRepository",
    "ReviewRepository",
]


