from typing import Dict, List, Optional, Any, Set
from bs4 import BeautifulSoup

from src.scraping.listing_parser import ListingParser
from src.logging_config import get_logger
logger = get_logger(__name__)

class ArchiveParser(ListingParser):
    """
    Parses archive page to extract review URLs.
    
    HTML structure to parse:
    <div class="archive">
        <a href="/category/pr/issue-179/">Issue 179</a>
        <a href="/category/pr/issue-178/">Issue 178</a>
        ...
    </div>
    """
    
    def __init__(self, archive_url: str = "https://platypus1917.org/platypus-review/", selectors: List[str] = None):
        """
        Initialize ArchiveParser with archive URL and selectors.
        
        Args:
            archive_url: URL of the archive page
            selectors: CSS selectors for finding review links (optional)
        """
        default_selectors = [ 
            'h2 > a[href^="https://platypus1917.org/category/pr/issue-"]',
        ]
        
        selectors = selectors or default_selectors
        super().__init__(base_url=archive_url, link_selectors=selectors)
        logger.info(f"ArchiveParser initialized with {len(selectors)} selectors")
        
    def parse_archive_page(self, html: str) -> List[str]:
        """
        Extract review URLs from archive.
        Delegates to inherited parse_listing_page.
        """
        logger.debug("Parsing archive page")
        urls = self.parse_listing_page(html)
        logger.info(f"Found {len(urls)} review URLs in archive")
        return urls