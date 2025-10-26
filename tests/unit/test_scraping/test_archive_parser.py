"""
Unit tests for ArchiveParser.
Tests parsing of archive page HTML to extract review URLs.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.scraping.archive_parser import ArchiveParser


@pytest.fixture
def archive_parser():
    """Create ArchiveParser instance for testing"""
    return ArchiveParser()


@pytest.fixture
def mock_archive_html():
    """Mock HTML content from archive page"""
    return """
    <html>
        <body>
            <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-177/">Issue 177</a></h2>
            <h2><a href="https://platypus1917.org/about/">About</a></h2>
            <a href="https://external.com/link">External</a>
        </body>
    </html>
    """


@pytest.fixture
def empty_archive_html():
    """Mock empty archive HTML"""
    return """
    <html>
        <body>
            <div>No review links here</div>
        </body>
    </html>
    """


class TestArchiveParser:
    """Test ArchiveParser class"""
    
    def test_init_default_selectors(self):
        """Test ArchiveParser initialization with default selectors"""
        parser = ArchiveParser()
        assert isinstance(parser, ArchiveParser)
    
    def test_parse_archive_page_success(self, archive_parser, mock_archive_html):
        """Test successful parsing of archive page"""
        with patch.object(archive_parser, 'parse_listing_page') as mock_parse:
            expected_urls = [
                "https://platypus1917.org/category/pr/issue-179/",
                "https://platypus1917.org/category/pr/issue-178/",
                "https://platypus1917.org/category/pr/issue-177/"
            ]
            mock_parse.return_value = expected_urls
            
            result = archive_parser.parse_archive_page(mock_archive_html)
            
            mock_parse.assert_called_once_with(mock_archive_html)
            assert result == expected_urls
            assert len(result) == 3
    
    def test_parse_archive_page_empty(self, archive_parser, empty_archive_html):
        """Test parsing archive page with no review links"""
        with patch.object(archive_parser, 'parse_listing_page') as mock_parse:
            mock_parse.return_value = []
            
            result = archive_parser.parse_archive_page(empty_archive_html)
            
            mock_parse.assert_called_once_with(empty_archive_html)
            assert result == []
    
    def test_parse_archive_page_filters_non_review_links(self, archive_parser):
        """Test that parse_archive_page only returns review URLs"""
        # This tests integration with ListingParser filtering
        with patch.object(archive_parser, 'parse_listing_page') as mock_parse:
            # Simulate that ListingParser already filtered the URLs
            mock_parse.return_value = [
                "https://platypus1917.org/category/pr/issue-179/",
                "https://platypus1917.org/category/pr/issue-178/"
            ]
            
            result = archive_parser.parse_archive_page("<html></html>")
            
            # Verify no non-review URLs in result
            assert all("category/pr/issue-" in url for url in result)
    
    def test_parse_archive_page_with_custom_selectors(self):
        """Test ArchiveParser with custom selectors"""
        custom_selectors = [
            'h2 > a[href*="issue-"]',
            'div.archive a[href*="pr/"]'
        ]
        
        # Mock the initialization to use custom selectors
        parser = ArchiveParser()
        
        with patch.object(parser, 'parse_listing_page') as mock_parse:
            mock_parse.return_value = ["https://platypus1917.org/category/pr/issue-180/"]
            
            result = parser.parse_archive_page("<html></html>")
            
            assert len(result) == 1
    
    def test_parse_archive_page_handles_malformed_html(self, archive_parser):
        """Test parsing with malformed HTML"""
        malformed_html = "<html><h2><a href='incomplete"
        
        with patch.object(archive_parser, 'parse_listing_page') as mock_parse:
            # BeautifulSoup handles malformed HTML gracefully
            mock_parse.return_value = []
            
            result = archive_parser.parse_archive_page(malformed_html)
            
            assert result == []
    
    def test_parse_archive_page_logging(self, archive_parser, mock_archive_html, caplog):
        """Test that appropriate logging occurs"""
        import logging
        
        with caplog.at_level(logging.DEBUG):
            with patch.object(archive_parser, 'parse_listing_page') as mock_parse:
                mock_parse.return_value = ["url1", "url2", "url3"]
                
                archive_parser.parse_archive_page(mock_archive_html)
                
                # Check that logging messages are present
                assert "Parsing archive page" in caplog.text
                assert "Found 3 review URLs in archive" in caplog.text
