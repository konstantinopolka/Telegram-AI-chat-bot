import pytest
import requests
from unittest.mock import patch

from src.scraping.review_fetcher import ReviewFetcher

class TestFetcher:
    """Test the predefined methods from the abstract Fetcher class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.fetcher = ReviewFetcher("https://platypus1917.org/platypus-review/")
    
    def test_validate_url_valid_urls(self):
        """Test validate_url with valid URLs"""
        valid_urls = [
            "https://example.com",
            "http://test.org/path",
            "https://platypus1917.org/platypus-review/",
            "http://localhost:8000/test"
        ]
        
        for url in valid_urls:
            assert self.fetcher.validate_url(url) == True, f"URL should be valid: {url}"
    
    def test_validate_url_invalid_urls(self):
        """Test validate_url with invalid URLs"""
        invalid_urls = [
            "",
            "not-a-url",
            "://example.com",     # Missing scheme
            "https://",           # Missing netloc
            "example.com",        # Missing scheme
            None
        ]
        
        for url in invalid_urls:
            if url is not None:
                assert self.fetcher.validate_url(url) == False, f"URL should be invalid: {url}"
    
    def test_validate_url_malformed(self):
        """Test validate_url with malformed URLs that cause exceptions"""
        # Test with non-string input that might cause parsing errors
        assert self.fetcher.validate_url(123) == False
        assert self.fetcher.validate_url([]) == False
        assert self.fetcher.validate_url({}) == False
    
    def test_handle_request_error_default(self):
        """Test the default error handling implementation"""
        error = requests.RequestException("Connection failed")
        url = "https://example.com"
        
        # Capture printed output - ReviewFetcher overrides with custom message
        with patch('builtins.print') as mock_print:
            self.fetcher.handle_request_error(error, url)
            mock_print.assert_called_once_with(f"Failed to fetch review from {url}: {error}")
