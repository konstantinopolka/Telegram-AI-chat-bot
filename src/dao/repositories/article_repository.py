from typing import Optional, List
from sqlmodel import select
from datetime import datetime, timedelta

from src.dao.models.article import Article
from src.dao.repositories.base_repository import BaseRepository
from src.logging_config import get_logger

logger = get_logger(__name__)


class ArticleRepository(BaseRepository[Article]):
    """Repository for Article model with domain-specific queries"""
    
    def __init__(self):
        super().__init__(Article)
        logger.info("ArticleRepository initialized")
    
    async def get_by_url(self, url: str) -> Optional[Article]:
        """
        Get article by original URL.
        
        Args:
            url: Original article URL
            
        Returns:
            Article instance or None
        """
        logger.debug(f"Fetching article by URL: {url}")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(Article).where(Article.original_url == url)
                )
                article = result.scalar_one_or_none()
                if article:
                    logger.debug(f"Found article: {article.title} (ID={article.id})")
                else:
                    logger.debug(f"No article found with URL: {url}")
                return article
        except Exception as e:
            logger.error(f"Failed to fetch article by URL {url}: {e}", exc_info=True)
            raise
    
    async def get_by_review_id(self, review_id: int) -> List[Article]:
        """
        Get all articles for a review.
        
        Args:
            review_id: Review ID
            
        Returns:
            List of articles
        """
        logger.debug(f"Fetching articles for review_id: {review_id}")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(Article).where(Article.review_id == review_id)
                )
                articles = result.scalars().all()
                logger.debug(f"Found {len(articles)} articles for review_id: {review_id}")
                return articles
        except Exception as e:
            logger.error(f"Failed to fetch articles for review_id {review_id}: {e}", exc_info=True)
            raise
    
    async def get_recent(self, limit: int = 10) -> List[Article]:
        """
        Get most recent articles.
        
        Args:
            limit: Maximum number of articles
            
        Returns:
            List of recent articles
        """
        logger.debug(f"Fetching {limit} most recent articles")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(Article)
                    .order_by(Article.created_at.desc())
                    .limit(limit)
                )
                articles = result.scalars().all()
                logger.debug(f"Retrieved {len(articles)} recent articles")
                return articles
        except Exception as e:
            logger.error(f"Failed to fetch recent articles: {e}", exc_info=True)
            raise
    
    async def search_by_title(self, search_term: str) -> List[Article]:
        """
        Search articles by title.
        
        Args:
            search_term: Search term (case-insensitive)
            
        Returns:
            List of matching articles
        """
        logger.debug(f"Searching articles by title: '{search_term}'")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(Article).where(
                        Article.title.ilike(f"%{search_term}%")
                    )
                )
                articles = result.scalars().all()
                logger.debug(f"Found {len(articles)} articles matching '{search_term}'")
                return articles
        except Exception as e:
            logger.error(f"Failed to search articles by title '{search_term}': {e}", exc_info=True)
            raise
    
    async def get_by_author(self, author_name: str) -> List[Article]:
        """
        Get articles by author name (searches JSON array).
        
        Args:
            author_name: Author name
            
        Returns:
            List of articles by author
        """
        logger.debug(f"Fetching articles by author: {author_name}")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(Article).where(
                        Article.authors.contains([author_name])
                    )
                )
                articles = result.scalars().all()
                logger.debug(f"Found {len(articles)} articles by author: {author_name}")
                return articles
        except Exception as e:
            logger.error(f"Failed to fetch articles by author {author_name}: {e}", exc_info=True)
            raise
    
    async def get_without_telegraph(self) -> List[Article]:
        """
        Get articles that haven't been published to Telegraph.
        
        Returns:
            List of unpublished articles
        """
        logger.debug("Fetching articles without Telegraph URLs")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(Article).where(
                        (Article.telegraph_urls == None) | 
                        (Article.telegraph_urls == [])
                    )
                )
                articles = result.scalars().all()
                logger.debug(f"Found {len(articles)} articles without Telegraph URLs")
                return articles
        except Exception as e:
            logger.error(f"Failed to fetch articles without Telegraph URLs: {e}", exc_info=True)
            raise
    
    async def update_telegraph_urls(
        self, 
        article_id: int, 
        telegraph_urls: List[str]
    ) -> Optional[Article]:
        """
        Update article's Telegraph URLs.
        
        Args:
            article_id: Article ID
            telegraph_urls: List of Telegraph URLs
            
        Returns:
            Updated Article or None if not found
        """
        logger.info(f"Updating Telegraph URLs for article_id {article_id}: {len(telegraph_urls)} URLs")
        try:
            article = await self.get_by_id(article_id)
            if article:
                article.telegraph_urls = telegraph_urls
                updated_article = await self.update(article)
                logger.info(f"Updated Telegraph URLs for article: {article.title}")
                return updated_article
            logger.warning(f"Cannot update Telegraph URLs - article not found: article_id={article_id}")
            return None
        except Exception as e:
            logger.error(f"Failed to update Telegraph URLs for article_id {article_id}: {e}", exc_info=True)
            raise


# Singleton instance
article_repository = ArticleRepository()
logger.info("ArticleRepository singleton instance created")