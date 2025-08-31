import pytest
import requests

from src.scraping.review_fetcher import ReviewFetcher

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

