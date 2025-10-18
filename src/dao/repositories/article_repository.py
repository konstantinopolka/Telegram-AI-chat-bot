from typing import Optional, List
from sqlmodel import select
from datetime import datetime, timedelta

from src.dao.models.article import Article
from src.dao.repositories.base_repository import BaseRepository


class ArticleRepository(BaseRepository[Article]):
    """Repository for Article model with domain-specific queries"""
    
    def __init__(self):
        super().__init__(Article)
    
    async def get_by_url(self, url: str) -> Optional[Article]:
        """
        Get article by original URL.
        
        Args:
            url: Original article URL
            
        Returns:
            Article instance or None
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(Article).where(Article.original_url == url)
            )
            return result.scalar_one_or_none()
    
    async def get_by_review_id(self, review_id: int) -> List[Article]:
        """
        Get all articles for a review.
        
        Args:
            review_id: Review ID
            
        Returns:
            List of articles
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(Article).where(Article.review_id == review_id)
            )
            return result.scalars().all()
    
    async def get_recent(self, limit: int = 10) -> List[Article]:
        """
        Get most recent articles.
        
        Args:
            limit: Maximum number of articles
            
        Returns:
            List of recent articles
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(Article)
                .order_by(Article.created_at.desc())
                .limit(limit)
            )
            return result.scalars().all()
    
    async def search_by_title(self, search_term: str) -> List[Article]:
        """
        Search articles by title.
        
        Args:
            search_term: Search term (case-insensitive)
            
        Returns:
            List of matching articles
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(Article).where(
                    Article.title.ilike(f"%{search_term}%")
                )
            )
            return result.scalars().all()
    
    async def get_by_author(self, author_name: str) -> List[Article]:
        """
        Get articles by author name (searches JSON array).
        
        Args:
            author_name: Author name
            
        Returns:
            List of articles by author
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(Article).where(
                    Article.authors.contains([author_name])
                )
            )
            return result.scalars().all()
    
    async def get_without_telegraph(self) -> List[Article]:
        """
        Get articles that haven't been published to Telegraph.
        
        Returns:
            List of unpublished articles
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(Article).where(
                    (Article.telegraph_urls == None) | 
                    (Article.telegraph_urls == [])
                )
            )
            return result.scalars().all()
    
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
        article = await self.get_by_id(article_id)
        if article:
            article.telegraph_urls = telegraph_urls
            return await self.update(article)
        return None


# Singleton instance
article_repository = ArticleRepository()