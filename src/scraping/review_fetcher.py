from typing import List, Optional, Dict, Any

import requests
from src.scraping import Fetcher


class ReviewFetcher(Fetcher):
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()  # Reuse connections
        
    # ===============================
    # FETCHING FUNCTIONS - Network operations
    # ===============================

    def fetch_page(self, url: str) -> str:
        """Fetch raw HTML content from a URL"""
        if not self.validate_url(url):
            raise ValueError(f"Invalid URL format: {url}")
        
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    
    def fetch_multiple_pages(self, urls: List[str]) -> Dict[str, str]:
        """Fetch multiple pages and return URL -> HTML mapping"""
        results = {}
        for url in urls:
            if not self.validate_url(url):
                print(f"Skipping invalid URL: {url}")
                continue
            try:
                html = self.fetch_page(url)
                results[url] = html
            except Exception as e:
                self.handle_request_error(e, url)
        return results
    

    def handle_request_error(self, error: Exception, url: str) -> None:
        """Custom error handling for review fetching"""
        print(f"Failed to fetch review from {url}: {error}")
    
    


