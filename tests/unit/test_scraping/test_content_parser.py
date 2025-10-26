import pytest
from bs4 import BeautifulSoup

from src.scraping.content_parser import ContentParser
from src.scraping.review_parser import ReviewParser


@pytest.fixture
def content_parser():
    """Create a concrete ContentParser implementation for testing"""
    return ReviewParser("https://platypus1917.org/platypus-review/")


class TestContentParserAbstract:
    """Test that ContentParser is properly abstract"""
    
    def test_cannot_instantiate_directly(self):
        """Test that ContentParser cannot be instantiated directly"""
        with pytest.raises(TypeError) as exc_info:
            ContentParser()
        
        # Verify it's because of abstract methods
        assert "Can't instantiate abstract class" in str(exc_info.value)
    
    def test_has_required_abstract_methods(self):
        """Test that ContentParser defines all required abstract methods"""
        expected_abstract_methods = {
            'parse_content_page',
            'extract_title',
            'extract_content',
            'extract_metadata',
            'clean_content_for_publishing'
        }
        
        actual_abstract_methods = set(ContentParser.__abstractmethods__)
        
        assert expected_abstract_methods.issubset(actual_abstract_methods)


class TestContentParserInheritance:
    """Test that ContentParser inherits from Parser correctly"""
    
    def test_inherits_from_parser(self):
        """Test that ContentParser inherits from Parser"""
        from src.scraping.parser import Parser
        assert issubclass(ContentParser, Parser)
    
    def test_concrete_implementation_has_parser_methods(self, content_parser):
        """Test that concrete implementations have Parser methods"""
        # Inherited from Parser
        assert hasattr(content_parser, 'create_soup')
        assert callable(content_parser.create_soup)
        
        assert hasattr(content_parser, 'normalize_url')
        assert callable(content_parser.normalize_url)
        
        assert hasattr(content_parser, 'clean_text')
        assert callable(content_parser.clean_text)
    
    def test_concrete_implementation_has_content_methods(self, content_parser):
        """Test that concrete implementations have ContentParser methods"""
        # Defined in ContentParser
        assert hasattr(content_parser, 'parse_content_page')
        assert callable(content_parser.parse_content_page)
        
        assert hasattr(content_parser, 'extract_title')
        assert callable(content_parser.extract_title)
        
        assert hasattr(content_parser, 'extract_content')
        assert callable(content_parser.extract_content)
        
        assert hasattr(content_parser, 'extract_metadata')
        assert callable(content_parser.extract_metadata)
        
        assert hasattr(content_parser, 'clean_content_for_publishing')
        assert callable(content_parser.clean_content_for_publishing)


class TestContentParserMethods:
    """Test that concrete implementations properly implement ContentParser methods"""
    
    def test_parse_content_page_returns_dict(self, content_parser):
        """Test that parse_content_page returns a dictionary"""
        html = """
        <html>
            <body>
                <div class="bpf-title"><h1>Test Title</h1></div>
                <div class="bpf-content">
                    <h2>by Test Author</h2>
                    <p>Test content</p>
                </div>
            </body>
        </html>
        """
        url = "https://platypus1917.org/2025/01/01/test-article"
        
        result = content_parser.parse_content_page(html, url)
        
        assert isinstance(result, dict)
        assert 'title' in result
        assert 'content' in result
        assert 'original_url' in result
    
    def test_extract_title_returns_string(self, content_parser):
        """Test that extract_title returns a string"""
        html = '<div class="bpf-title"><h1>Test Title</h1></div>'
        soup = content_parser.create_soup(html)
        
        title = content_parser.extract_title(soup)
        
        assert isinstance(title, str)
        assert len(title) > 0
    
    def test_extract_content_returns_string(self, content_parser):
        """Test that extract_content returns a string"""
        html = '<div class="bpf-content"><p>Test content</p></div>'
        soup = content_parser.create_soup(html)
        
        content = content_parser.extract_content(soup)
        
        assert isinstance(content, str)
    
    def test_extract_metadata_returns_dict(self, content_parser):
        """Test that extract_metadata returns a dictionary"""
        html = """
        <html>
            <body>
                <div class="bpf-content">
                    <h2>by Test Author</h2>
                    <div class="has-text-align-right">Test Category | January 2025</div>
                </div>
            </body>
        </html>
        """
        soup = content_parser.create_soup(html)
        url = "https://platypus1917.org/2025/01/01/test-article"
        
        metadata = content_parser.extract_metadata(soup, url)
        
        assert isinstance(metadata, dict)
    
    def test_clean_content_for_publishing_returns_string(self, content_parser):
        """Test that clean_content_for_publishing returns a string"""
        html = '<div><p>Clean content</p><script>alert("bad")</script></div>'
        soup = content_parser.create_soup(html)
        content_div = soup.find('div')
        
        cleaned = content_parser.clean_content_for_publishing(content_div)
        
        assert isinstance(cleaned, str)
        # Should not contain script tags
        assert '<script>' not in cleaned
