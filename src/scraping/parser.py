from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from bs4 import BeautifulSoup

class Parser(ABC):
    

    
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