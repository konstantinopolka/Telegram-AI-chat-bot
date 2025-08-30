from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from bs4 import BeautifulSoup

class Parser(ABC):
    
    @abstractmethod
    def parse_listing_page(self, html: str) -> List[str]:
        """Parse a listing/index page to extract content URLs"""
        pass
    
    @abstractmethod
    def parse_content_page(self, html: str, url: str) -> Dict[str, Any]:
        """Parse a content page to extract structured data"""
        pass
    
    @abstractmethod
    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract title from parsed HTML"""
        pass
    
    @abstractmethod
    def extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from parsed HTML"""
        pass
    
    @abstractmethod
    def extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract metadata (authors, dates, etc.) from parsed HTML"""
        pass
    
    @abstractmethod
    def clean_content_for_publishing(self, content_div) -> str:
        """Clean content for publishing platform compatibility"""
        pass
    
    # Optional: methods that might have default implementations
    def create_soup(self, html: str) -> BeautifulSoup:
        """Create BeautifulSoup object - standard implementation"""
        return BeautifulSoup(html, 'html.parser')
    
    def normalize_url(self, url: str, base_url: str) -> str:
        """Normalize relative URLs to absolute"""
        from urllib.parse import urljoin
        return urljoin(base_url, url) if url.startswith('/') else url
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        return ' '.join(text.split()).strip()