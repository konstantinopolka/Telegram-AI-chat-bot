import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from typing import List, Optional, Dict, Any

from src.scraping.fetcher import Fetcher
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


class TestReviewFetcher:
    """Test the ReviewFetcher concrete implementation"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.base_url = "https://platypus1917.org/platypus-review/"
        self.fetcher = ReviewFetcher(self.base_url)
    
    def test_init(self):
        """Test ReviewFetcher initialization"""
        assert self.fetcher.base_url == self.base_url
        assert isinstance(self.fetcher.session, requests.Session)
    
    @patch('requests.Session.get')
    def test_fetch_page_success(self, mock_get):
        """Test successful page fetching"""
        # Mock successful response
        mock_response = Mock()
        mock_response.text = "<html><body>Test content</body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        url = "https://example.com/test"
        result = self.fetcher.fetch_page(url)
        
        assert result == "<html><body>Test content</body></html>"
        mock_get.assert_called_once_with(url, timeout=10)
        mock_response.raise_for_status.assert_called_once()
    
    def test_fetch_page_invalid_url(self):
        """Test fetch_page with invalid URL"""
        invalid_url = "not-a-url"
        
        with pytest.raises(ValueError, match="Invalid URL format"):
            self.fetcher.fetch_page(invalid_url)
    
    @patch('requests.Session.get')
    def test_fetch_page_http_error(self, mock_get):
        """Test fetch_page with HTTP error"""
        # Mock HTTP error response
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        url = "https://example.com/notfound"
        
        with pytest.raises(requests.HTTPError):
            self.fetcher.fetch_page(url)
    
    @patch('requests.Session.get')
    def test_fetch_page_timeout(self, mock_get):
        """Test fetch_page with timeout"""
        mock_get.side_effect = requests.Timeout("Request timed out")
        
        url = "https://example.com/slow"
        
        with pytest.raises(requests.Timeout):
            self.fetcher.fetch_page(url)
    
    @patch.object(ReviewFetcher, 'fetch_page')
    def test_fetch_multiple_pages_success(self, mock_fetch_page):
        """Test successful fetching of multiple pages"""
        # Mock fetch_page to return different content for different URLs
        def side_effect(url):
            if "page1" in url:
                return "<html>Page 1 content</html>"
            elif "page2" in url:
                return "<html>Page 2 content</html>"
            return "<html>Default content</html>"
        
        mock_fetch_page.side_effect = side_effect
        
        urls = [
            "https://example.com/page1",
            "https://example.com/page2"
        ]
        
        result = self.fetcher.fetch_multiple_pages(urls)
        
        expected = {
            "https://example.com/page1": "<html>Page 1 content</html>",
            "https://example.com/page2": "<html>Page 2 content</html>"
        }
        
        assert result == expected
        assert mock_fetch_page.call_count == 2
    
    @patch.object(ReviewFetcher, 'fetch_page')
    @patch.object(ReviewFetcher, 'handle_request_error')
    def test_fetch_multiple_pages_with_errors(self, mock_handle_error, mock_fetch_page):
        """Test fetch_multiple_pages with some URLs failing"""
        # Mock fetch_page to succeed for first URL, fail for second
        def side_effect(url):
            if "page1" in url:
                return "<html>Page 1 content</html>"
            elif "page2" in url:
                raise requests.RequestException("Failed to fetch")
            return "<html>Default content</html>"
        
        mock_fetch_page.side_effect = side_effect
        
        urls = [
            "https://example.com/page1",
            "https://example.com/page2"
        ]
        
        result = self.fetcher.fetch_multiple_pages(urls)
        
        # Should only contain successful result
        expected = {
            "https://example.com/page1": "<html>Page 1 content</html>"
        }
        
        assert result == expected
        mock_handle_error.assert_called_once()
    
    def test_fetch_multiple_pages_invalid_urls(self):
        """Test fetch_multiple_pages with invalid URLs"""
        urls = [
            "https://example.com/valid",
            "invalid-url",
            "another-invalid"
        ]
        
        with patch.object(self.fetcher, 'fetch_page') as mock_fetch_page:
            mock_fetch_page.return_value = "<html>Valid content</html>"
            
            with patch('builtins.print') as mock_print:
                result = self.fetcher.fetch_multiple_pages(urls)
                
                # Should only fetch the valid URL
                assert len(result) == 1
                assert "https://example.com/valid" in result
                
                # Should print warnings for invalid URLs
                assert mock_print.call_count == 2
                mock_print.assert_any_call("Skipping invalid URL: invalid-url")
                mock_print.assert_any_call("Skipping invalid URL: another-invalid")
    
    def test_handle_request_error_custom(self):
        """Test ReviewFetcher's custom error handling"""
        error = requests.ConnectionError("Connection failed")
        url = "https://example.com"
        
        with patch('builtins.print') as mock_print:
            self.fetcher.handle_request_error(error, url)
            mock_print.assert_called_once_with(f"Failed to fetch review from {url}: {error}")


class TestReviewFetcherIntegration:
    """Integration tests for ReviewFetcher (these require network access)"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.fetcher = ReviewFetcher("https://httpbin.org")  # Using httpbin for reliable testing
    
    @pytest.mark.integration
    def test_fetch_page_real_request(self):
        """Test fetch_page with a real HTTP request"""
        # Skip if running without internet access
        pytest.importorskip("requests")
        
        try:
            result = self.fetcher.fetch_page("https://httpbin.org/html")
            assert "<html>" in result
            assert len(result) > 0
        except requests.RequestException:
            pytest.skip("Network not available for integration test")
    
    @pytest.mark.integration
    def test_fetch_multiple_pages_real_requests(self):
        """Test fetch_multiple_pages with real HTTP requests"""
        pytest.importorskip("requests")
        
        urls = [
            "https://httpbin.org/html",
            "https://httpbin.org/json"
        ]
        
        try:
            result = self.fetcher.fetch_multiple_pages(urls)
            assert len(result) == 2
            assert all(len(content) > 0 for content in result.values())
        except requests.RequestException:
            pytest.skip("Network not available for integration test")


class TestReviewFetcherAbstractMethods:
    """Test that ReviewFetcher implements required abstract methods"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.fetcher = ReviewFetcher("https://example.com")
    
    def test_implements_abstract_methods(self):
        """Test that all abstract methods are implemented"""
        # These methods should exist and be callable
        assert hasattr(self.fetcher, 'fetch_page')
        assert callable(self.fetcher.fetch_page)
        
        assert hasattr(self.fetcher, 'fetch_multiple_pages')
        assert callable(self.fetcher.fetch_multiple_pages)
        

