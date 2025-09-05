import pytest
import requests
from unittest.mock import patch

from src.scraping.review_fetcher import ReviewFetcher

@pytest.fixture
def fetcher():
    return ReviewFetcher("https://platypus1917.org/platypus-review/")

class TestFetcher:
    """Test the predefined methods from the abstract Fetcher class"""
        
    @pytest.mark.parametrize("valid_url", [
            "https://example.com",
            "http://test.org/path",
            "https://platypus1917.org/platypus-review/",
            "http://localhost:8000/test"
        ])
    def test_validate_url_valid_urls(self, fetcher, valid_url):
        """Test validate_url with valid URLs"""
        assert fetcher.validate_url(valid_url) == True, f"URL should be valid: {valid_url}"
            
    @pytest.mark.parametrize("invalid_url", 
            [
            "", 
            "not-a-url",
            "://example.com",     # Missing scheme
            "https://",           # Missing netloc
            "example.com",        # Missing scheme
            None
        ])
    def test_validate_url_invalid_urls(self, fetcher, invalid_url):
        """Test validate_url with invalid URLs"""
        assert fetcher.validate_url(invalid_url) == False, f"URL should be invalid: {invalid_url}"
    
    @pytest.mark.parametrize("malformed_url", 
        [
        123, 
        [],
        {} 
    ])
    def test_validate_url_malformed(self, fetcher, malformed_url):
        """Test validate_url with malformed URLs that cause exceptions"""
        # Test with non-string input that might cause parsing errors
        assert fetcher.validate_url(malformed_url) == False
    
    def test_handle_request_error_default(self, fetcher):
        """Test the default error handling implementation"""
        error = requests.RequestException("Connection failed")
        url = "https://example.com"
        
        # Capture printed output - ReviewFetcher overrides with custom message
        with patch('builtins.print') as mock_print:
            fetcher.handle_request_error(error, url)
            mock_print.assert_called_once_with(f"Failed to fetch review from {url}: {error}")
