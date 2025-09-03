import pytest
import requests
from unittest.mock import Mock, patch

from src.scraping.review_fetcher import ReviewFetcher

@pytest.fixture(scope="class")
def fetcher():
    base_url = "https://platypus1917.org/platypus-review/"
    f = ReviewFetcher(base_url)

    # --- setup complete ---
    yield f

    # --- teardown logic ---
    f.session.close()   # cleanup: close the requests.Session

class TestReviewFetcher:
    """Test the ReviewFetcher concrete implementation"""
    
    # def setup_method(self):
    #     """Set up test fixtures"""
    #     self.base_url = "https://platypus1917.org/platypus-review/"
    #     fetcher = ReviewFetcher(self.base_url)
    
    def test_init(self, fetcher):
        """Test ReviewFetcher initialization"""
        assert fetcher.base_url == "https://platypus1917.org/platypus-review/"
        assert isinstance(fetcher.session, requests.Session)
    
    @patch('requests.Session.get')
    def test_fetch_page_success(self, mock_get, fetcher):
        """Test successful page fetching"""
        # Mock successful response
        mock_response = Mock()
        mock_response.text = "<html><body>Test content</body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        url = "https://example.com/test"
        result = fetcher.fetch_page(url)
        
        assert result == "<html><body>Test content</body></html>"
        mock_get.assert_called_once_with(url, timeout=10)
        mock_response.raise_for_status.assert_called_once()
    
    def test_fetch_page_invalid_url(self, fetcher):
        """Test fetch_page with invalid URL"""
        invalid_url = "not-a-url"
        
        with pytest.raises(ValueError, match="Invalid URL format"):
            fetcher.fetch_page(invalid_url)
    
    @patch('requests.Session.get')
    def test_fetch_page_http_error(self, mock_get, fetcher):
        """Test fetch_page with HTTP error"""
        # Mock HTTP error response
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        url = "https://example.com/notfound"
        
        with pytest.raises(requests.HTTPError):
            fetcher.fetch_page(url)
    
    @patch('requests.Session.get')
    def test_fetch_page_timeout(self, mock_get, fetcher):
        """Test fetch_page with timeout"""
        mock_get.side_effect = requests.Timeout("Request timed out")
        
        url = "https://example.com/slow"
        
        with pytest.raises(requests.Timeout):
            fetcher.fetch_page(url)
    
    @patch.object(ReviewFetcher, 'fetch_page')
    def test_fetch_multiple_pages_success(self, mock_fetch_page, fetcher):
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
        
        result = fetcher.fetch_multiple_pages(urls)
        
        expected = {
            "https://example.com/page1": "<html>Page 1 content</html>",
            "https://example.com/page2": "<html>Page 2 content</html>"
        }
        
        assert result == expected
        assert mock_fetch_page.call_count == 2
    
    @patch.object(ReviewFetcher, 'fetch_page')
    @patch.object(ReviewFetcher, 'handle_request_error')
    def test_fetch_multiple_pages_with_errors(self, mock_handle_error, mock_fetch_page, fetcher):
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
        
        result = fetcher.fetch_multiple_pages(urls)
        
        # Should only contain successful result
        expected = {
            "https://example.com/page1": "<html>Page 1 content</html>"
        }
        
        assert result == expected
        mock_handle_error.assert_called_once()
    
    def test_fetch_multiple_pages_invalid_urls(self, fetcher):
        """Test fetch_multiple_pages with invalid URLs"""
        urls = [
            "https://example.com/valid",
            "invalid-url",
            "another-invalid"
        ]
        
        with patch.object(fetcher, 'fetch_page') as mock_fetch_page:
            mock_fetch_page.return_value = "<html>Valid content</html>"
            
            with patch('builtins.print') as mock_print:
                result = fetcher.fetch_multiple_pages(urls)
                
                # Should only fetch the valid URL
                assert len(result) == 1
                assert "https://example.com/valid" in result
                
                # Should print warnings for invalid URLs
                assert mock_print.call_count == 2
                mock_print.assert_any_call("Skipping invalid URL: invalid-url")
                mock_print.assert_any_call("Skipping invalid URL: another-invalid")
    
    def test_handle_request_error_custom(self, fetcher):
        """Test ReviewFetcher's custom error handling"""
        error = requests.ConnectionError("Connection failed")
        url = "https://example.com"
        
        with patch('builtins.print') as mock_print:
            fetcher.handle_request_error(error, url)
            mock_print.assert_called_once_with(f"Failed to fetch review from {url}: {error}")
            
    def test_implements_abstract_methods(self, fetcher):
        """Test that all abstract methods are implemented"""
        # These methods should exist and be callable
        assert hasattr(fetcher, 'fetch_page')
        assert callable(fetcher.fetch_page)
        
        assert hasattr(fetcher, 'fetch_multiple_pages')
        assert callable(fetcher.fetch_multiple_pages)


