from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.logging_config import get_logger
import requests


logger = get_logger(__name__)


class Fetcher():
    
    def __init__(self, base_url: str):
        logger.info(f"Initializing Fetcher for: {base_url}")
        self.base_url = base_url
        self.session = requests.Session()  # Reuse connections
        logger.debug("HTTP session created for connection pooling")
        
    def fetch_page(self, url: Optional[str] = None) -> str:
        """Fetch raw HTML content from a URL
        
        Args:
            url: The URL to fetch. If None, uses the base_url.
            
        Returns:
            str: The raw HTML content of the page.
        """
        if url is None:
            url = self.base_url
            
        logger.debug(f"Fetching page: {url}")
        
        if not self.validate_url(url):
            error_msg = f"Invalid URL format: {url}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.debug(f"Sending GET request to: {url}")
        try:
            response = self.session.get(url, timeout=10)
            logger.debug(f"Response received: status={response.status_code}, size={len(response.text)} chars")
            response.raise_for_status()
            logger.debug(f"Successfully fetched page from: {url}")
            return response.text
        except requests.exceptions.Timeout:
            logger.error(f"Timeout while fetching: {url}", exc_info=True)
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}", exc_info=True)
            raise
    
    def fetch_multiple_pages(self, urls: List[str]) -> Dict[str, str]:
        """Fetch multiple pages and return URL -> HTML mapping"""
        logger.info(f"Fetching {len(urls)} pages")
        results = {}
        
        for idx, url in enumerate(urls, 1):
            logger.debug(f"Fetching page {idx}/{len(urls)}: {url}")
            
            if not self.validate_url(url):
                logger.warning(f"Skipping invalid URL ({idx}/{len(urls)}): {url}")
                continue
                
            try:
                html = self.fetch_page(url)
                results[url] = html
                logger.debug(f"Successfully fetched page {idx}/{len(urls)}")
            except Exception as e:
                logger.error(f"Failed to fetch page {idx}/{len(urls)}", exc_info=True)
                self.handle_request_error(e, url)
                
        logger.info(f"Successfully fetched {len(results)}/{len(urls)} pages")
        return results
    
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