"""
Service class for scanning the Review archive.
Identifies new reviews by comparing archive URLs with database.
Does NOT handle scraping details (delegates to ArchiveScraper).
"""

from typing import Dict, List, Optional, Set
from src.dao import review_repository
from src.scraping.archive_scraper import ArchiveScraper

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
        
        
    async def scan_for_new_reviews(self) -> Dict[str, List[str]]:
        """
        Scan archive and categorize reviews.
        
        Returns:
            {
                'new_reviews': [url1, url2, ...],      # Not in DB
                'existing_reviews': [url3, url4, ...], # Already in DB
                'total_count': int
            }
        """
        new_reviews: Set[str] = None
        existing_reviews: Set[str] = None
        
        archive_urls: Set[str] = self.archive_scraper.get_listing_urls()
        archive_urls_dict: Dict[str, bool] = self._check_reviews_in_db(archive_urls)
        # TO-DO: either I can make a query in the database to get a set with all existing reviews
        # or I can check every url from the archive through the database by passing to the review repo
        
        total_count = len(archive_urls)
        return {
            'new_reviews': new_reviews,
            'existing_reviews': existing_reviews,
            'total_count': total_count
            }
    
    
    async def get_review_by_criteria(self, 
                                     review_id: Optional[int] = None,
                                     month: Optional[str] = None) -> Optional[str]:
        """
        Find review URL by ID or month.
        First checks DB, if not found checks archive.
        
        Args:
            review_id: Review ID (e.g., 179)
            month: Month string (e.g., "October 2025")
            
        Returns:
            Review URL if found, None otherwise
        """
        
        # TO-DO, do I really need this method? Because it looks like a database operation!
        pass
    
    async def _check_reviews_in_db(self, archive_urls: Set[str]) -> Dict[str, bool]:
        """
        Check which review URLs exist in database.
        
        Returns:
            {url: exists_in_db, ...}
        """
        database_review_urls: Set[str] = None
        # TO-DO: either I can make a query in the database to get a set with all existing reviews
        # or I can check every url from the archive through the database by passing to the review repo
        
        
        archive_urls_dict: Dict[str, bool] = None
    
        return archive_urls_dict