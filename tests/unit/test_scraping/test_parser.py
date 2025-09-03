import pytest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup

from src.scraping.parser import Parser
from src.scraping.review_parser import ReviewParser


class TestParser:
    """Test the predefined methods from the abstract Parser class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.parser = ReviewParser("https://platypus1917.org/platypus-review/")
    
    def test_create_soup(self):
        """Test create_soup creates BeautifulSoup object correctly"""
        html = "<html><body><h1>Test</h1></body></html>"
        soup = self.parser.create_soup(html)
        
        assert isinstance(soup, BeautifulSoup)
        assert soup.find('h1').get_text() == "Test"
        assert soup.name == "[document]"
    
    def test_create_soup_with_complex_html(self):
        """Test create_soup with more complex HTML"""
        html = """
        <html>
            <head><title>Test Page</title></head>
            <body>
                <div class="content">
                    <p>Paragraph 1</p>
                    <p>Paragraph 2</p>
                </div>
            </body>
        </html>
        """
        soup = self.parser.create_soup(html)
        
        assert soup.title.get_text() == "Test Page"
        assert len(soup.find_all('p')) == 2
        assert soup.select_one('.content') is not None
        
    @pytest.mark.parametrize(
        "base_url, relative_url, expected_url",
        [
            ("https://example.com/base",  "/articles/123", "https://example.com/articles/123"), # Relative URL starting with /
            ("https://example.com/base", "articles/123", "articles/123")  # Relative URL without leading / (returns as-is in current implementation)
        ]
    )
    def test_normalize_url_relative_urls(self, base_url, relative_url, expected_url):
        """Test normalize_url with relative URLs"""
        result = self.parser.normalize_url(relative_url, base_url)
        assert result == expected_url
    @pytest.mark.parametrize(
        
    )
    def test_normalize_url_absolute_urls(self, base_url, ):
        """Test normalize_url with absolute URLs"""
        base_url = "https://example.com/base"
        
        # Absolute URL should remain unchanged
        absolute_url = "https://other-site.com/article"
        result = self.parser.normalize_url(absolute_url, base_url)
        assert result == absolute_url
        
        # HTTP URL should remain unchanged
        http_url = "http://example.com/article"
        result = self.parser.normalize_url(http_url, base_url)
        assert result == http_url
    
    def test_normalize_url_complex_base_urls(self):
        """Test normalize_url with complex base URLs"""
        base_url = "https://example.com/section/subsection/"
        
        # Relative URL with parent directory reference
        relative_url = "/new-section/article"
        result = self.parser.normalize_url(relative_url, base_url)
        assert result == "https://example.com/new-section/article"
    
    def test_clean_text_whitespace_normalization(self):
        """Test clean_text normalizes whitespace correctly"""
        # Multiple spaces
        text = "Hello    world"
        result = self.parser.clean_text(text)
        assert result == "Hello world"
        
        # Leading and trailing whitespace
        text = "  Hello world  "
        result = self.parser.clean_text(text)
        assert result == "Hello world"
        
        # Newlines and tabs
        text = "Hello\n\tworld\r\n"
        result = self.parser.clean_text(text)
        assert result == "Hello world"
    
    def test_clean_text_empty_and_special_cases(self):
        """Test clean_text with empty and special cases"""
        # Empty string
        assert self.parser.clean_text("") == ""
        
        # Only whitespace
        assert self.parser.clean_text("   \n\t  ") == ""
        
        # Single word
        assert self.parser.clean_text("Hello") == "Hello"
        
        # Multiple newlines
        text = "Line1\n\n\nLine2"
        result = self.parser.clean_text(text)
        assert result == "Line1 Line2"


class TestParserAbstractMethods:
    """Test that Parser is properly abstract and methods raise NotImplementedError"""
    
    def test_cannot_instantiate_abstract_parser(self):
        """Test that Parser cannot be instantiated directly"""
        with pytest.raises(TypeError):
            Parser("https://example.com")
    
    def test_abstract_methods_exist(self):
        """Test that all abstract methods are defined"""
        # Check that abstract methods are defined in the class
        abstract_methods = {
            'parse_listing_page',
            'parse_content_page', 
            'extract_title',
            'extract_content',
            'extract_metadata',
            'clean_content_for_publishing'
        }
        
        # Get all abstract methods from the Parser class
        parser_abstracts = set(Parser.__abstractmethods__)
        
        # Verify all expected methods are abstract
        assert abstract_methods.issubset(parser_abstracts)
    
    def test_concrete_methods_exist(self):
        """Test that concrete methods are available"""
        # These should be callable on a concrete implementation
        parser = ReviewParser("https://example.com")
        
        assert hasattr(parser, 'create_soup')
        assert callable(parser.create_soup)
        
        assert hasattr(parser, 'normalize_url')
        assert callable(parser.normalize_url)
        
        assert hasattr(parser, 'clean_text')
        assert callable(parser.clean_text)


class TestParserUtilityMethods:
    """Test utility methods behavior in different scenarios"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.parser = ReviewParser("https://platypus1917.org/platypus-review/")
    
    def test_create_soup_with_malformed_html(self):
        """Test create_soup handles malformed HTML gracefully"""
        malformed_html = "<html><body><p>Unclosed paragraph<div>Mixed tags</p></div></body></html>"
        soup = self.parser.create_soup(malformed_html)
        
        # BeautifulSoup should parse it without crashing
        assert isinstance(soup, BeautifulSoup)
        # Should be able to find elements
        assert soup.find('p') is not None
        assert soup.find('div') is not None
    
    def test_create_soup_with_empty_html(self):
        """Test create_soup with empty or minimal HTML"""
        # Empty string
        soup = self.parser.create_soup("")
        assert isinstance(soup, BeautifulSoup)
        
        # Minimal HTML
        soup = self.parser.create_soup("<html></html>")
        assert isinstance(soup, BeautifulSoup)
        assert soup.html is not None
    
    def test_normalize_url_edge_cases(self):
        """Test normalize_url with edge cases"""
        base_url = "https://example.com"
        
        # Empty URL (returns as-is in current implementation)
        result = self.parser.normalize_url("", base_url)
        assert result == ""  # Current implementation returns empty string as-is
        
        # Just a slash
        result = self.parser.normalize_url("/", base_url)
        assert result == "https://example.com/"
        
        # Fragment URL (returns as-is in current implementation)
        result = self.parser.normalize_url("#section", base_url)
        assert result == "#section"  # Current implementation returns fragment as-is
        
        # Query parameters (returns as-is in current implementation)
        result = self.parser.normalize_url("?param=value", base_url)
        assert result == "?param=value"  # Current implementation returns query as-is
    
    def test_clean_text_unicode_handling(self):
        """Test clean_text with Unicode characters"""
        # Unicode characters
        text = "Héllo wörld"
        result = self.parser.clean_text(text)
        assert result == "Héllo wörld"
        
        # Mixed Unicode and ASCII
        text = "Hello 世界"
        result = self.parser.clean_text(text)
        assert result == "Hello 世界"
        
        # Unicode whitespace
        text = "Hello\u00A0world"  # Non-breaking space
        result = self.parser.clean_text(text)
        assert result == "Hello world"
    
    def test_clean_text_preserves_meaningful_content(self):
        """Test that clean_text preserves meaningful content"""
        # Should preserve punctuation
        text = "Hello, world! How are you?"
        result = self.parser.clean_text(text)
        assert result == "Hello, world! How are you?"
        
        # Should preserve numbers
        text = "The year  2025   is here"
        result = self.parser.clean_text(text)
        assert result == "The year 2025 is here"
        
        # Should preserve special characters
        text = "Email: user@example.com"
        result = self.parser.clean_text(text)
        assert result == "Email: user@example.com"
