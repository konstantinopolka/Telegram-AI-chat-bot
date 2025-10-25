"""
Concrete scraper for the Review archive page.
Extracts review URLs from the archive section.
"""

from typing import Dict, List, Optional, Any

from .scraper import Scraper

class ArchiveScraper(Scraper):
    """
    Scraper for archive page - extracts review URLs only.
    
    Note: Unlike ReviewScraper, this does NOT scrape article content.
    It only extracts review listing URLs from the archive page.
    """
    
    def __init__(self, archive_url: str):
        self.archive_url: str = archive_url
        """Initialize with archive page URL"""
        
    def get_listing_urls(self) -> List[str]:
        """
        Get all review URLs from archive page.
        
        Implementation:
        1. Fetch archive page HTML (via ArchiveFetcher)
        2. Parse archive section (via ArchiveParser)
        3. Extract review URLs
        4. Return list of review URLs
        """
        pass
        
    def scrape_single_article(self, url: str) -> Optional[Dict[str, Any]]:
        """Not used for archive - raises NotImplementedError"""
        raise NotImplementedError("Archive scraper only extracts URLs")
        
    def scrape_review_batch(self) -> List[str]:
        """
        Main method: get all review URLs from archive.
        Returns list of review URLs (not full review data).
        """
        pass