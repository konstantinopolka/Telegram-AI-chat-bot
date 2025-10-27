"""
Service class for scanning the Review archive.
Identifies new reviews by comparing archive URLs with database.
Does NOT handle scraping details (delegates to ArchiveScraper).
"""

from typing import Dict, List, Optional, Set
from src.dao import review_repository
from src.scraping.archive_scraper import ArchiveScraper

from src.logging_config import get_logger

logger = get_logger(__name__)

from dotenv import load_dotenv
import os
load_dotenv()

class ArchiveScanner:
    
    """
    Scans review archive and identifies new/existing reviews.
    Workflow:
    1. Get all review URLs from archive (via ArchiveScraper)
    3. Return lists of new vs existing review URLs
    
    2. Check which reviews exist in database
    """
    
    
    def __init__(self, archive_url: str | None = None):
        """Initialize with archive page URL"""
        self.archive_url: str = archive_url or os.getenv("ARCHIVE_URL", "")
        self.archive_scraper: ArchiveScraper =  ArchiveScraper(self.archive_url)
        logger.info(f"ArchiveScanner initialized for: {self.archive_url}")
        
    async def get_new_reviews(self) -> Set[str]:
        logger.info("Getting new review URLs")
        reviews_dict: Dict[str, Set[str]] = await self.scan_for_new_reviews()
        new_reviews: Set[str] = reviews_dict.get("new_reviews")
        logger.info(f"Found {len(new_reviews)} new review(s)")
        return new_reviews
        
        
    async def scan_for_new_reviews(self) -> Dict[str, Set[str]]:
        """
        Scan archive and categorize reviews.
        
        Returns:
            {
                'new_reviews': [url1, url2, ...],      # Not in DB
                'existing_reviews': [url3, url4, ...], # Already in DB
                'total_count': int
            }
        """
        # Get all URLs from archive
        logger.info("Starting archive scan for new reviews")
        archive_urls: Set[str] = self.archive_scraper.get_listing_urls()
        logger.info(f"Found {len(archive_urls)} review URLs in archive")
        
        # Check which ones exist in database
        logger.debug("Checking which reviews exist in database")
        existing_db_urls: Set[str] = await self._check_reviews_in_db(archive_urls)
        logger.info(f"Found {len(existing_db_urls)} existing reviews in database")
        
        
        # Calculate new vs existing
        new_reviews: Set[str] = archive_urls - existing_db_urls
        existing_reviews: Set[str] = archive_urls & existing_db_urls
        
        logger.info(f"Scan complete: {len(new_reviews)} new, {len(existing_reviews)} existing")
        total_count = len(archive_urls)
        
        return {
            'new_reviews': new_reviews,
            'existing_reviews': existing_reviews,
            'total_count': total_count
            }
    
    
    async def get_review_by_criteria(self, review_id: Optional[int] = None, month: Optional[str] = None) -> Optional[str]:
        """
        Find review URL by ID or month.
        First checks DB, if not found checks archive.
        
        Args:
            review_id: Review ID (e.g., 179)
            month: Month string (e.g., "October 2025")
            
        Returns:
            Review URL if found, None otherwise
        """
        logger.info(f"Looking for review by criteria: review_id={review_id}, month={month}")
        
        # First check database
        if review_id:
            review = await review_repository.get_by_id(review_id)
            if review:
                logger.info(f"Found review in database: {review.source_url}")
                return review.source_url
        
        # If not in DB, search archive
        # This would require extending ArchiveScraper to get review metadata
        # TO-DO: For now, return None - implement later if needed
        logger.warning("Review not found in database, archive search not yet implemented")
        return None
    
    async def _check_reviews_in_db(self, archive_urls: Set[str]) -> Set[str]:
        """
        Check which review URLs exist in database using BULK query (efficient).
        
        Args:
            archive_urls: Set of URLs from archive
            
        Returns:
            Set of URLs that exist in database
        """
        logger.debug(f"Checking {len(archive_urls)} URLs against database")
        
        database_review_urls: Set[str] = await review_repository.get_all_source_urls()
        
        # Find intersection - which archive URLs exist in DB
        existing_urls = archive_urls & database_review_urls
        
        logger.debug(f"Found {len(existing_urls)} URLs already in database")
        return existing_urls