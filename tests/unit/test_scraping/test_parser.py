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
        "base_url, absolute_url, expected_url",
        [
            ("https://example.com/base", "https://other-site.com/article", "https://other-site.com/article"),  # HTTPS absolute URL
            ("https://example.com/base", "http://example.com/article", "http://example.com/article"),  # HTTP absolute URL
            ("https://example.com/base", "https://example.com/other/page", "https://example.com/other/page"),  # Same domain absolute URL
            ("http://test.com", "https://external.org/path", "https://external.org/path")  # Different protocol and domain
        ]
    )
    def test_normalize_url_absolute_urls(self, base_url, absolute_url, expected_url):
        """Test normalize_url with absolute URLs"""
        result = self.parser.normalize_url(absolute_url, base_url)
        assert result == expected_url
    
    @pytest.mark.parametrize(
        "base_url, relative_url, expected_url",
        [
            ("https://example.com/section/subsection/", "/new-section/article", "https://example.com/new-section/article"),  # Complex base with relative
            ("https://example.com/path/to/page", "/different/path", "https://example.com/different/path"),  # Nested path base
            ("https://subdomain.example.com/api/v1/", "/endpoint", "https://subdomain.example.com/endpoint"),  # Subdomain with API path
            ("https://example.com:8080/app/", "/resource", "https://example.com:8080/resource")  # Base with port
        ]
    )
    def test_normalize_url_complex_base_urls(self, base_url, relative_url, expected_url):
        """Test normalize_url with complex base URLs"""
        result = self.parser.normalize_url(relative_url, base_url)
        assert result == expected_url
    
    @pytest.mark.parametrize(
        "input_text, expected_result",
        [
            ("Hello    world", "Hello world"),  # Multiple spaces
            ("  Hello world  ", "Hello world"),  # Leading and trailing whitespace
            ("Hello\n\tworld\r\n", "Hello world"),  # Newlines and tabs
            ("Hello\n\n\nworld", "Hello world"),  # Multiple newlines
            ("Hello\t\t\tworld", "Hello world"),  # Multiple tabs
            ("  \t  Hello  \n  world  \r  ", "Hello world"),  # Mixed whitespace
            ("Hello\u00A0world", "Hello world")  # Non-breaking space
        ]
    )
    def test_clean_text_whitespace_normalization(self, input_text, expected_result):
        """Test clean_text normalizes whitespace correctly"""
        result = self.parser.clean_text(input_text)
        assert result == expected_result
    
    @pytest.mark.parametrize(
        "input_text, expected_result",
        [
            ("", ""),  # Empty string
            ("   \n\t  ", ""),  # Only whitespace
            ("Hello", "Hello"),  # Single word
            ("Line1\n\n\nLine2", "Line1 Line2"),  # Multiple newlines
            ("Word", "Word"),  # Single word no whitespace
            ("\n\n\n", ""),  # Only newlines
            ("\t\t\t", ""),  # Only tabs
            ("  A  ", "A")  # Single character with whitespace
        ]
    )
    def test_clean_text_empty_and_special_cases(self, input_text, expected_result):
        """Test clean_text with empty and special cases"""
        result = self.parser.clean_text(input_text)
        assert result == expected_result


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
    
    @pytest.mark.parametrize(
        "html_input, expected_result",
        [
            ("", True),  # Empty string should create valid soup
            ("<html></html>", True),  # Minimal HTML should create valid soup with html element
            ("<html><body></body></html>", True),  # Basic structure
            ("   ", True),  # Whitespace only
            ("<p>Text</p>", True),  # Fragment without html tag
        ]
    )
    def test_create_soup_with_empty_html(self, html_input, expected_result):
        """Test create_soup with empty or minimal HTML"""
        soup = self.parser.create_soup(html_input)
        assert isinstance(soup, BeautifulSoup) == expected_result
        
        # Additional checks for non-empty HTML
        if html_input.strip() and "<html>" in html_input:
            assert soup.html is not None
    
    @pytest.mark.parametrize(
        "base_url, test_url, expected_result",
        [
            ("https://example.com", "", ""),  # Empty URL (returns as-is)
            ("https://example.com", "/", "https://example.com/"),  # Just a slash
            ("https://example.com", "#section", "#section"),  # Fragment URL (returns as-is)
            ("https://example.com", "?param=value", "?param=value"),  # Query parameters (returns as-is)
            ("https://example.com", "javascript:void(0)", "javascript:void(0)"),  # JavaScript URL (returns as-is)
            ("https://example.com/path", "/new-path", "https://example.com/new-path"),  # Absolute path
            ("https://example.com", "//other.com/path", "//other.com/path"),  # Protocol-relative URL (returns as-is)
        ]
    )
    def test_normalize_url_edge_cases(self, base_url, test_url, expected_result):
        """Test normalize_url with edge cases"""
        result = self.parser.normalize_url(test_url, base_url)
        assert result == expected_result
    
    @pytest.mark.parametrize(
        "input_text, expected_result",
        [
            ("Héllo wörld", "Héllo wörld"),  # Unicode characters
            ("Hello 世界", "Hello 世界"),  # Mixed Unicode and ASCII
            ("Hello\u00A0world", "Hello world"),  # Non-breaking space
            ("Café résumé naïve", "Café résumé naïve"),  # Accented characters
            ("🌟 Hello 🌟", "🌟 Hello 🌟"),  # Emoji
            ("Здравствуй мир", "Здравствуй мир"),  # Cyrillic
            ("مرحبا بالعالم", "مرحبا بالعالم"),  # Arabic
        ]
    )
    def test_clean_text_unicode_handling(self, input_text, expected_result):
        """Test clean_text with Unicode characters"""
        result = self.parser.clean_text(input_text)
        assert result == expected_result
    
    @pytest.mark.parametrize(
        "input_text, expected_result",
        [
            ("Hello, world! How are you?", "Hello, world! How are you?"),  # Punctuation
            ("The year  2025   is here", "The year 2025 is here"),  # Numbers with extra spaces
            ("Email: user@example.com", "Email: user@example.com"),  # Special characters
            ("Price: $19.99 (USD)", "Price: $19.99 (USD)"),  # Currency symbols
            ("Version 2.0.1-beta", "Version 2.0.1-beta"),  # Version numbers
            ("Path: /home/user/file.txt", "Path: /home/user/file.txt"),  # File paths
            ("URL: https://example.com?q=test", "URL: https://example.com?q=test"),  # URLs
            ("Math: 2 + 2 = 4", "Math: 2 + 2 = 4"),  # Mathematical expressions
        ]
    )
    def test_clean_text_preserves_meaningful_content(self, input_text, expected_result):
        """Test that clean_text preserves meaningful content"""
        result = self.parser.clean_text(input_text)
        assert result == expected_result
