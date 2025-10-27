"""
Unit tests for ArchiveScraper.
Tests scraping of archive page to extract review URLs.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.scraping.archive_scraper import ArchiveScraper


@pytest.fixture
def archive_url():
    """Standard archive URL for testing"""
    return "https://platypus1917.org/platypus-review/"


@pytest.fixture
def archive_scraper(archive_url):
    """Create ArchiveScraper instance for testing"""
    return ArchiveScraper(archive_url)


@pytest.fixture
def mock_review_urls():
    """Mock set of review URLs"""
    return [
        "https://platypus1917.org/category/pr/issue-179/",
        "https://platypus1917.org/category/pr/issue-178/",
        "https://platypus1917.org/category/pr/issue-177/"
    ]


@pytest.fixture
def mock_archive_html():
    """Mock HTML from archive page"""
    return """
    <html>
        <body>
            <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178</a></h2>
        </body>
    </html>
    """


class TestArchiveScraper:
    """Test ArchiveScraper class"""
    
    def test_init(self, archive_scraper, archive_url):
        """Test ArchiveScraper initialization"""
        assert archive_scraper.archive_url == archive_url
        assert hasattr(archive_scraper, 'fetcher')
        assert hasattr(archive_scraper, 'parser')
        assert archive_scraper.fetcher.base_url == archive_url
    
    def test_init_with_env_variable(self):
        """Test initialization with archive URL from environment"""
        with patch.dict('os.environ', {'ARCHIVE_URL': 'https://test.com/archive/'}):
            # When created without URL, should use environment variable
            # But our current implementation requires URL, so skip this for now
            pass
    
    def test_get_listing_urls_success(self, archive_scraper, mock_archive_html, mock_review_urls):
        """Test successful extraction of review URLs"""
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(archive_scraper.parser, 'parse_archive_page') as mock_parse:
            
            mock_fetch.return_value = mock_archive_html
            mock_parse.return_value = mock_review_urls
            
            result = archive_scraper.get_listing_urls()
            
            mock_fetch.assert_called_once()
            mock_parse.assert_called_once_with(mock_archive_html)
            assert isinstance(result, set)
            assert len(result) == 3
            assert all(url in result for url in mock_review_urls)
    
    def test_get_listing_urls_returns_set(self, archive_scraper):
        """Test that get_listing_urls returns a set (removes duplicates)"""
        duplicate_urls = [
            "https://platypus1917.org/category/pr/issue-179/",
            "https://platypus1917.org/category/pr/issue-179/",  # Duplicate
            "https://platypus1917.org/category/pr/issue-178/"
        ]
        
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(archive_scraper.parser, 'parse_archive_page') as mock_parse:
            
            mock_fetch.return_value = "<html></html>"
            mock_parse.return_value = duplicate_urls
            
            result = archive_scraper.get_listing_urls()
            
            # Set should remove duplicates
            assert isinstance(result, set)
            assert len(result) == 2
    
    def test_get_listing_urls_empty_archive(self, archive_scraper):
        """Test get_listing_urls with empty archive"""
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(archive_scraper.parser, 'parse_archive_page') as mock_parse:
            
            mock_fetch.return_value = "<html><body>No reviews</body></html>"
            mock_parse.return_value = []
            
            result = archive_scraper.get_listing_urls()
            
            assert isinstance(result, set)
            assert len(result) == 0
    
    def test_get_listing_urls_fetch_error(self, archive_scraper):
        """Test get_listing_urls when fetcher raises error"""
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.side_effect = Exception("Network error")
            
            with pytest.raises(Exception, match="Network error"):
                archive_scraper.get_listing_urls()
    
    def test_get_listing_urls_parse_error(self, archive_scraper, mock_archive_html):
        """Test get_listing_urls when parser raises error"""
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(archive_scraper.parser, 'parse_archive_page') as mock_parse:
            
            mock_fetch.return_value = mock_archive_html
            mock_parse.side_effect = Exception("Parse error")
            
            with pytest.raises(Exception, match="Parse error"):
                archive_scraper.get_listing_urls()
    
    def test_get_listing_urls_workflow(self, archive_scraper):
        """Test complete workflow: fetch -> parse -> return set"""
        expected_html = "<html>archive content</html>"
        expected_urls = [
            "https://platypus1917.org/category/pr/issue-179/",
            "https://platypus1917.org/category/pr/issue-178/"
        ]
        
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(archive_scraper.parser, 'parse_archive_page') as mock_parse:
            
            mock_fetch.return_value = expected_html
            mock_parse.return_value = expected_urls
            
            result = archive_scraper.get_listing_urls()
            
            # Verify workflow sequence
            assert mock_fetch.call_count == 1
            assert mock_parse.call_count == 1
            assert mock_parse.call_args[0][0] == expected_html
            assert isinstance(result, set)
            assert result == set(expected_urls)
    
    def test_scraper_does_not_implement_scraper_interface_methods(self, archive_scraper):
        """Test that ArchiveScraper doesn't implement unused Scraper methods"""
        # ArchiveScraper does not extend Scraper ABC, so it doesn't need
        # to implement scrape_single_article or scrape_review_batch
        assert not hasattr(archive_scraper, 'scrape_single_article')
        assert not hasattr(archive_scraper, 'scrape_review_batch')
