import pytest
import requests
from unittest.mock import Mock, patch

from src.scraping.fetcher import Fetcher

@pytest.fixture(scope="class")
def fetcher():
    base_url = "https://platypus1917.org/platypus-review/"
    f = Fetcher(base_url)

    # --- setup complete ---
    yield f

    # --- teardown logic ---
    f.session.close()   # cleanup: close the requests.Session

class TestFetcherDetailed:
    """Test the Fetcher class in detail"""
    
    def test_init(self, fetcher):
        """Test Fetcher initialization"""
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
    
    @patch('requests.Session.get')
    def test_fetch_page_no_url_uses_base(self, mock_get, fetcher):
        """Test fetch_page without URL parameter uses base_url"""
        # Mock successful response
        mock_response = Mock()
        mock_response.text = "<html><body>Base URL content</body></html>"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = fetcher.fetch_page()
        
        assert result == "<html><body>Base URL content</body></html>"
        mock_get.assert_called_once_with(fetcher.base_url, timeout=10)
    
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
        mock_response.text = "Error page content"
        mock_response.status_code = 404
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
    
    @patch.object(Fetcher, 'fetch_page')
    def test_fetch_multiple_pages_success(self, mock_fetch_page, fetcher):
        """Test successful fetching of multiple pages"""
        # Mock fetch_page to return different content for different URLs
        def side_effect(url=None):
            if url and "page1" in url:
                return "<html>Page 1 content</html>"
            elif url and "page2" in url:
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
    
    @patch.object(Fetcher, 'fetch_page')
    @patch.object(Fetcher, 'handle_request_error')
    def test_fetch_multiple_pages_with_errors(self, mock_handle_error, mock_fetch_page, fetcher):
        """Test fetch_multiple_pages with some URLs failing"""
        # Mock fetch_page to succeed for first URL, fail for second
        def side_effect(url=None):
            if url and "page1" in url:
                return "<html>Page 1 content</html>"
            elif url and "page2" in url:
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
            
            result = fetcher.fetch_multiple_pages(urls)
            
            # Should only fetch the valid URL
            assert len(result) == 1
            assert "https://example.com/valid" in result
            
            # Invalid URLs should be skipped (logged as warnings)
            assert mock_fetch_page.call_count == 1
    
    def test_handle_request_error(self, fetcher):
        """Test Fetcher's error handling"""
        error = requests.ConnectionError("Connection failed")
        url = "https://example.com"
        
        # The default implementation just logs the error
        # No assertion needed - just verify it doesn't raise an exception
        fetcher.handle_request_error(error, url)
            
    def test_has_required_methods(self, fetcher):
        """Test that all required methods are implemented"""
        # These methods should exist and be callable
        assert hasattr(fetcher, 'fetch_page')
        assert callable(fetcher.fetch_page)
        
        assert hasattr(fetcher, 'fetch_multiple_pages')
        assert callable(fetcher.fetch_multiple_pages)
        
        assert hasattr(fetcher, 'validate_url')
        assert callable(fetcher.validate_url)
        
        assert hasattr(fetcher, 'handle_request_error')
        assert callable(fetcher.handle_request_error)



