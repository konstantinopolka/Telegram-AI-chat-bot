from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.logging_config import get_logger

logger = get_logger(__name__)


class Fetcher(ABC):
    
    @abstractmethod
    def fetch_page(self, url: str) -> str:
        """Fetch raw HTML content from a URL"""
        pass
    
    @abstractmethod
    def fetch_multiple_pages(self, urls: List[str]) -> Dict[str, str]:
        """Fetch multiple pages and return URL -> HTML mapping"""
        pass
    
    # Optional: methods that might have default implementations
    def validate_url(self, url: str) -> bool:
        """Validate if URL is properly formatted"""
        try:
            from urllib.parse import urlparse
            result = urlparse(url)
            return all([result.scheme, result.netloc]) # all returns true only if all items are truthy
        except Exception:
            return False
    
    def handle_request_error(self, error: Exception, url: str) -> None:
        """Handle request errors - can be overridden"""
        logger.error(f"Request failed for {url}: {error}", exc_info=True)