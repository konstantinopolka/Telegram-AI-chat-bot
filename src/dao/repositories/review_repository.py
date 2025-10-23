from typing import Optional, List, override
from sqlmodel import select
from sqlalchemy.orm import selectinload

from src.dao.models.review import Review
from src.dao.repositories.base_repository import BaseRepository
from src.logging_config import get_logger

logger = get_logger(__name__)


class ReviewRepository(BaseRepository[Review]):
    """Repository for Review model with domain-specific queries"""
    
    def __init__(self):
        super().__init__(Review)
        logger.info("ReviewRepository initialized")
    

    async def get(self, obj: Review) -> Optional[Review]:
        """
        Get review by natural key (business ID).
        
        For reviews, the natural key is the review ID itself -
        it comes from the source (issue number) and defines uniqueness.
        """
        if obj.id is None:
            logger.warning("Cannot check natural key for Review without ID")
            return None
        
        return await self.get_by_id(obj.id)
    @override
    async def get_by_url(self, url: str) -> Optional[Review]:
        """
        Get review by source URL.
        
        Args:
            url: Review source URL
            
        Returns:
            Review instance or None
        """
        logger.debug(f"Fetching review by URL: {url}")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(Review).where(Review.source_url == url)
                )
                review = result.scalar_one_or_none()
                if review:
                    logger.debug(f"Found review with ID: {review.id}")
                else:
                    logger.debug(f"No review found with URL: {url}")
                return review
        except Exception as e:
            logger.error(f"Failed to fetch review by URL {url}: {e}", exc_info=True)
            raise
    
    async def get_with_articles(self, review_id: int) -> Optional[Review]:
        """
        Get review with all related articles eagerly loaded.
        
        Args:
            review_id: Review ID
            
        Returns:
            Review with articles relationship loaded
        """
        logger.debug(f"Fetching review with articles: review_id={review_id}")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(Review)
                    .options(selectinload(Review.articles))
                    .where(Review.id == review_id)
                )
                review = result.scalar_one_or_none()
                if review:
                    article_count = len(review.articles) if review.articles else 0
                    logger.debug(f"Found review with {article_count} articles (ID={review_id})")
                else:
                    logger.debug(f"No review found with ID: {review_id}")
                return review
        except Exception as e:
            logger.error(f"Failed to fetch review with articles (ID {review_id}): {e}", exc_info=True)
            raise
    
    async def get_recent(self, limit: int = 10) -> List[Review]:
        """
        Get most recent reviews.
        
        Args:
            limit: Maximum number of reviews
            
        Returns:
            List of recent reviews
        """
        logger.debug(f"Fetching {limit} most recent reviews")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(Review)
                    .order_by(Review.created_at.desc())
                    .limit(limit)
                )
                reviews = result.scalars().all()
                logger.debug(f"Retrieved {len(reviews)} recent reviews")
                return reviews
        except Exception as e:
            logger.error(f"Failed to fetch recent reviews: {e}", exc_info=True)
            raise
    @override
    def _get_identifier_for_logging(self, obj: Review, existing: Review = None) -> str:
        """Get meaningful identifier for logging."""
        target = existing if existing else obj
        return f"Issue ID={target.id}, URL={target.source_url}"
# Singleton instance
review_repository = ReviewRepository()
logger.info("ReviewRepository singleton instance created")