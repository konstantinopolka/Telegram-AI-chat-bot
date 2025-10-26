#standard libraries
from typing import List, Optional


from src.scraping.parser import Parser


class ListingParser(Parser):
    def __init__(self, base_url: str, link_selectors: List[str]):
        """
        Args:
            base_url: Base URL for normalizing relative links
            link_selectors: CSS selectors to find links (tried in order)
        """
        self.base_url = base_url
        self.link_selectors = link_selectors
        
    def parse_listing_page(self, html: str) -> List[str]:
        """
        Parse listing page HTML to extract URLs using configured selectors.
        Default implementation - can be overridden if needed.
        """
        soup = self.create_soup(html)
        urls = []
        
        for selector in self.link_selectors:
            links = soup.select(selector)
            extracted = [url for link in links if (url := self.extract_link(link))]
            urls.extend(extracted)
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(urls))
    def extract_link(self, link) -> Optional[str]:
        """Extract and normalize href from link element"""
        href = link.get('href')
        if href:
            return self.normalize_url(href, self.base_url)
        return None