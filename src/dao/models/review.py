from typing import Optional, List
from sqlmodel import select
from sqlalchemy.orm import selectinload

from src.dao.models.review import Review
from src.dao.repositories.base_repository import BaseRepository


class ReviewRepository(BaseRepository[Review]):
    """Repository for Review model with domain-specific queries"""
    
    def __init__(self):
        super().__init__(Review)
    
    async def get_by_url(self, url: str) -> Optional[Review]:
        """
        Get review by source URL.
        
        Args:
            url: Review source URL
            
        Returns:
            Review instance or None
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(Review).where(Review.source_url == url)
            )
            return result.scalar_one_or_none()
    
    async def get_with_articles(self, review_id: int) -> Optional[Review]:
        """
        Get review with all related articles eagerly loaded.
        
        Args:
            review_id: Review ID
            
        Returns:
            Review with articles relationship loaded
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(Review)
                .options(selectinload(Review.articles))
                .where(Review.id == review_id)
            )
            return result.scalar_one_or_none()
    
    async def get_recent(self, limit: int = 10) -> List[Review]:
        """
        Get most recent reviews.
        
        Args:
            limit: Maximum number of reviews
            
        Returns:
            List of recent reviews
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(Review)
                .order_by(Review.created_at.desc())
                .limit(limit)
            )
            return result.scalars().all()
    
    async def create_review(self, source_url: str) -> Review:
        """
        Create a new review.
        
        Args:
            source_url: Review source URL
            
        Returns:
            Created Review instance
        """
        review = Review(source_url=source_url)
        return await self.create(review)


# Singleton instance
review_repository = ReviewRepository()