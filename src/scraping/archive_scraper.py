"""
Concrete scraper for the Review archive page.
Extracts review URLs from the archive section.
"""

from typing import Dict, List, Optional, Any, Set
from src.scraping.fetcher import Fetcher


from src.scraping.fetcher import Fetcher
from src.scraping.archive_parser import ArchiveParser



class ArchiveScraper():
    """
    Scraper for archive page - extracts review URLs only.
    
    Note: Unlike ReviewScraper, this does NOT scrape article content.
    It only extracts review listing URLs from the archive page.
    """
    
    def __init__(self, archive_url: str) :
        self.archive_url = archive_url
        self.fetcher: Fetcher = Fetcher(archive_url)
        self.parser: ArchiveParser = ArchiveParser()
        """Initialize with archive page URL"""
        
    def get_listing_urls(self) -> Set[str]:
        """
        Get all review URLs from archive page.
        
        Implementation:
        1. Fetch archive page HTML (via ArchiveFetcher)
        2. Parse archive section (via ArchiveParser)
        3. Extract review URLs
        4. Return list of review URLs
        """
        
        archive_html: str = self.fetcher.fetch_page()
        # TO-DO: make a list of urls to a set to make sure there are no duplicates  
        archive_urls: Set[str] = self.parser.parse_archive_page(archive_html)
        return archive_urls
        