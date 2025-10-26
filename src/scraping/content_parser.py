from abc import abstractmethod
from typing import Dict, Any

from bs4 import BeautifulSoup

from src.scraping.parser import Parser

class ContentParser(Parser):
    """Base parser for content pages (articles, reviews, etc.)"""
    
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
    def extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract metadata (authors, dates, etc.) from parsed HTML"""
        pass
    
    @abstractmethod
    def clean_content_for_publishing(self, content_div) -> str:
        """Clean content for publishing platform compatibility"""
        pass
    
    