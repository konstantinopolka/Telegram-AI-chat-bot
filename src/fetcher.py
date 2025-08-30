from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class Fetcher(ABC):
    
    @abstractmethod
    def fetch_page(self, url: str) -> str:
        """Fetch raw HTML content from a URL"""
        pass
    
    @abstractmethod
    def fetch_multiple_pages(self, urls: List[str]) -> Dict[str, str]:
        """Fetch multiple pages and return URL -> HTML mapping"""
        pass
    
    @abstractmethod
    def get_listing_urls(self) -> List[str]:
        """Get URLs from a listing/index page"""
        pass
    
    @abstractmethod
    def get_content_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Complete workflow: fetch and parse content from URL"""
        pass
    
    # Optional: methods that might have default implementations
    def validate_url(self, url: str) -> bool:
        """Validate if URL is properly formatted"""
        try:
            from urllib.parse import urlparse
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def handle_request_error(self, error: Exception, url: str) -> None:
        """Handle request errors - can be overridden"""
        print(f"Request failed for {url}: {error}")