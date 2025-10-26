import pytest
from unittest.mock import Mock
from bs4 import BeautifulSoup

from src.scraping.listing_parser import ListingParser


@pytest.fixture
def listing_parser():
    """Create a ListingParser instance for testing"""
    selectors = ['h4 > a[href^="/20"]', 'a.article-link']
    return ListingParser(
        base_url="https://platypus1917.org/platypus-review/",
        link_selectors=selectors
    )


class TestListingParserInitialization:
    """Test ListingParser initialization"""
    
    def test_initialization_with_selectors(self):
        """Test that ListingParser initializes with provided selectors"""
        selectors = ['a.link', 'div > a']
        parser = ListingParser(
            base_url="https://example.com",
            link_selectors=selectors
        )
        
        assert parser.base_url == "https://example.com"
        assert parser.link_selectors == selectors
    
    def test_initialization_stores_base_url(self, listing_parser):
        """Test that base URL is stored correctly"""
        assert listing_parser.base_url == "https://platypus1917.org/platypus-review/"


class TestParseListingPage:
    """Test parse_listing_page method"""
    
    def test_parse_listing_page_with_single_selector(self):
        """Test parsing with a single selector"""
        html = """
        <html>
            <body>
                <h4><a href="/2025/01/article1">Article 1</a></h4>
                <h4><a href="/2025/01/article2">Article 2</a></h4>
            </body>
        </html>
        """
        
        parser = ListingParser(
            base_url="https://example.com",
            link_selectors=['h4 > a[href^="/20"]']
        )
        
        urls = parser.parse_listing_page(html)
        
        assert len(urls) == 2
        assert "https://example.com/2025/01/article1" in urls
        assert "https://example.com/2025/01/article2" in urls
    
    def test_parse_listing_page_with_multiple_selectors(self):
        """Test parsing with multiple selectors"""
        html = """
        <html>
            <body>
                <h4><a href="/2025/01/article1">Article 1</a></h4>
                <div><a class="article-link" href="/2025/01/article2">Article 2</a></div>
            </body>
        </html>
        """
        
        parser = ListingParser(
            base_url="https://example.com",
            link_selectors=['h4 > a', 'a.article-link']
        )
        
        urls = parser.parse_listing_page(html)
        
        assert len(urls) == 2
        assert "https://example.com/2025/01/article1" in urls
        assert "https://example.com/2025/01/article2" in urls
    
    def test_parse_listing_page_removes_duplicates(self):
        """Test that duplicate URLs are removed"""
        html = """
        <html>
            <body>
                <h4><a href="/2025/01/article1">Article 1</a></h4>
                <h4><a href="/2025/01/article1">Article 1 Again</a></h4>
                <div><a href="/2025/01/article1">Article 1 Third</a></div>
            </body>
        </html>
        """
        
        parser = ListingParser(
            base_url="https://example.com",
            link_selectors=['h4 > a', 'div > a']
        )
        
        urls = parser.parse_listing_page(html)
        
        assert len(urls) == 1
        assert urls[0] == "https://example.com/2025/01/article1"
    
    def test_parse_listing_page_preserves_order(self):
        """Test that URLs maintain order when duplicates are removed"""
        html = """
        <html>
            <body>
                <a href="/article1">Article 1</a>
                <a href="/article2">Article 2</a>
                <a href="/article1">Article 1 Again</a>
                <a href="/article3">Article 3</a>
            </body>
        </html>
        """
        
        parser = ListingParser(
            base_url="https://example.com",
            link_selectors=['a']
        )
        
        urls = parser.parse_listing_page(html)
        
        assert len(urls) == 3
        assert urls[0] == "https://example.com/article1"
        assert urls[1] == "https://example.com/article2"
        assert urls[2] == "https://example.com/article3"
    
    def test_parse_listing_page_with_empty_html(self, listing_parser):
        """Test parsing empty HTML returns empty list"""
        urls = listing_parser.parse_listing_page("")
        assert urls == []
    
    def test_parse_listing_page_with_no_matches(self, listing_parser):
        """Test parsing HTML with no matching selectors"""
        html = "<html><body><p>No links here</p></body></html>"
        urls = listing_parser.parse_listing_page(html)
        assert urls == []
    
    def test_parse_listing_page_absolute_urls(self):
        """Test parsing with absolute URLs"""
        html = """
        <html>
            <body>
                <a href="https://example.com/article1">Article 1</a>
                <a href="https://example.com/article2">Article 2</a>
            </body>
        </html>
        """
        
        parser = ListingParser(
            base_url="https://example.com",
            link_selectors=['a']
        )
        
        urls = parser.parse_listing_page(html)
        
        assert len(urls) == 2
        assert "https://example.com/article1" in urls
        assert "https://example.com/article2" in urls


class TestExtractLink:
    """Test extract_link method"""
    
    def test_extract_link_with_valid_href(self, listing_parser):
        """Test extracting link from element with href"""
        soup = BeautifulSoup('<a href="/article">Link</a>', 'html.parser')
        link_element = soup.find('a')
        
        url = listing_parser.extract_link(link_element)
        
        assert url == "https://platypus1917.org/article"
    
    def test_extract_link_with_absolute_url(self, listing_parser):
        """Test extracting absolute URL"""
        soup = BeautifulSoup('<a href="https://other.com/article">Link</a>', 'html.parser')
        link_element = soup.find('a')
        
        url = listing_parser.extract_link(link_element)
        
        assert url == "https://other.com/article"
    
    def test_extract_link_without_href(self, listing_parser):
        """Test extracting link from element without href returns None"""
        soup = BeautifulSoup('<a>Link without href</a>', 'html.parser')
        link_element = soup.find('a')
        
        url = listing_parser.extract_link(link_element)
        
        assert url is None
    
    def test_extract_link_with_empty_href(self, listing_parser):
        """Test extracting link with empty href"""
        soup = BeautifulSoup('<a href="">Empty Link</a>', 'html.parser')
        link_element = soup.find('a')
        
        url = listing_parser.extract_link(link_element)
        
        # Empty href returns None in the current implementation
        # (urljoin with empty string returns empty string, which is falsy)
        assert url is None or url == ""


class TestListingParserInheritance:
    """Test that ListingParser inherits from Parser correctly"""
    
    def test_inherits_create_soup(self, listing_parser):
        """Test that create_soup is inherited"""
        html = "<html><body><h1>Test</h1></body></html>"
        soup = listing_parser.create_soup(html)
        
        assert isinstance(soup, BeautifulSoup)
        assert soup.find('h1').get_text() == "Test"
    
    def test_inherits_normalize_url(self, listing_parser):
        """Test that normalize_url is inherited"""
        url = listing_parser.normalize_url("/article", "https://example.com")
        assert url == "https://example.com/article"
    
    def test_inherits_clean_text(self, listing_parser):
        """Test that clean_text is inherited"""
        text = listing_parser.clean_text("  Hello   world  ")
        assert text == "Hello world"
