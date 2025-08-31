import pytest
import re
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup

from src.scraping.parser import Parser
from src.scraping.review_parser import ReviewParser


class TestReviewParser:
    """Test the ReviewParser concrete implementation"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.base_url = "https://platypus1917.org/platypus-review/"
        self.parser = ReviewParser(self.base_url)
    
    def test_init(self):
        """Test ReviewParser initialization"""
        assert self.parser.base_url == self.base_url
        assert isinstance(self.parser, Parser)
    
    def test_parse_listing_page_success(self):
        """Test successful parsing of listing page"""
        html = """
        <html>
            <body>
                <h4><a href="https://platypus1917.org/2025/01/01/article1/">Article 1</a></h4>
                <h4><a href="https://platypus1917.org/2024/12/15/article2/">Article 2</a></h4>
                <h4><a href="https://example.com/external/">External Link</a></h4>
                <h4><a href="/relative/link/">Relative Link</a></h4>
            </body>
        </html>
        """
        
        result = self.parser.parse_listing_page(html)
        
        # Should only include Platypus articles from 20xx years
        expected_urls = [
            "https://platypus1917.org/2025/01/01/article1/",
            "https://platypus1917.org/2024/12/15/article2/"
        ]
        assert result == expected_urls
    
    def test_parse_listing_page_empty_html(self):
        """Test parsing of empty listing page"""
        html = "<html><body></body></html>"
        result = self.parser.parse_listing_page(html)
        assert result == []
    
    def test_parse_listing_page_no_matching_links(self):
        """Test parsing when no links match the pattern"""
        html = """
        <html>
            <body>
                <h4><a href="https://other-site.com/article/">Other Site</a></h4>
                <h4><a href="https://platypus1917.org/about/">About Page</a></h4>
            </body>
        </html>
        """
        result = self.parser.parse_listing_page(html)
        assert result == []
    
    def test_parse_content_page_success(self):
        """Test successful parsing of content page"""
        url = "https://platypus1917.org/2025/01/01/test-article/"
        
        with patch.object(self.parser, 'extract_title') as mock_title, \
             patch.object(self.parser, 'extract_content') as mock_content, \
             patch.object(self.parser, 'extract_metadata') as mock_metadata:
            
            mock_title.return_value = "Test Article"
            mock_content.return_value = "<p>Test content</p>"
            mock_metadata.return_value = {
                'authors': ['John Doe'],
                'published_date': 'January 2025',
                'review_id': 173
            }
            
            result = self.parser.parse_content_page("<html>test</html>", url)
            
            expected = {
                'title': 'Test Article',
                'content': '<p>Test content</p>',
                'original_url': url,
                'authors': ['John Doe'],
                'published_date': 'January 2025',
                'review_id': 173
            }
            
            assert result == expected
    
    def test_extract_title_success(self):
        """Test successful title extraction"""
        html = "<html><body><h1>  Test Article Title  </h1></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser.extract_title(soup)
        assert result == "Test Article Title"
    
    def test_extract_title_no_h1(self):
        """Test title extraction when no h1 exists"""
        html = "<html><body><h2>Not a title</h2></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser.extract_title(soup)
        assert result == "Untitled"
    
    def test_extract_content_with_wrapper(self):
        """Test content extraction with dc-page-seo-wrapper"""
        html = """
        <html>
            <body>
                <div class="dc-page-seo-wrapper">
                    <p>Main content here</p>
                    <div>More content</div>
                </div>
                <div class="sidebar">Sidebar content</div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        with patch.object(self.parser, 'clean_content_for_publishing') as mock_clean:
            mock_clean.return_value = "cleaned content"
            result = self.parser.extract_content(soup)
            
            # Should pass the dc-page-seo-wrapper div to cleaning
            mock_clean.assert_called_once()
            args = mock_clean.call_args[0]
            assert args[0].get('class') == ['dc-page-seo-wrapper']
            assert result == "cleaned content"
    
    def test_extract_content_fallback_to_full_soup(self):
        """Test content extraction fallback when no wrapper found"""
        html = "<html><body><p>Content without wrapper</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        with patch.object(self.parser, 'clean_content_for_publishing') as mock_clean:
            mock_clean.return_value = "cleaned content"
            result = self.parser.extract_content(soup)
            
            # Should pass the entire soup to cleaning
            mock_clean.assert_called_once()
            args = mock_clean.call_args[0]
            assert args[0].name == "[document]"  # BeautifulSoup document
            assert result == "cleaned content"
    
    def test_extract_metadata_success(self):
        """Test successful metadata extraction"""
        soup = Mock()
        
        with patch.object(self.parser, '_extract_authors') as mock_authors, \
             patch.object(self.parser, '_extract_date') as mock_date, \
             patch.object(self.parser, '_extract_id') as mock_id:
            
            mock_authors.return_value = ['Author 1', 'Author 2']
            mock_date.return_value = 'February 2025'
            mock_id.return_value = 173
            
            result = self.parser.extract_metadata(soup)
            
            expected = {
                'authors': ['Author 1', 'Author 2'],
                'published_date': 'February 2025',
                'review_id': 173
            }
            
            assert result == expected
            mock_authors.assert_called_once_with(soup)
            mock_date.assert_called_once_with(soup)
            mock_id.assert_called_once_with(soup)


class TestReviewParserCleanContent:
    """Test the clean_content_for_publishing method"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.parser = ReviewParser("https://example.com")
    
    def test_clean_content_removes_unwanted_elements(self):
        """Test that unwanted elements are removed"""
        html = """
        <div>
            <p>Keep this paragraph</p>
            <nav>Remove this nav</nav>
            <footer>Remove this footer</footer>
            <div class="sidebar">Remove this sidebar</div>
            <script>alert('remove this');</script>
            <style>body { color: red; }</style>
            <div class="comments">Remove comments</div>
        </div>
        """
        content_div = BeautifulSoup(html, 'html.parser').find('div')
        
        result = self.parser.clean_content_for_publishing(content_div)
        
        # Should keep the paragraph
        assert '<p>Keep this paragraph</p>' in result
        # Should remove unwanted elements
        assert 'nav' not in result
        assert 'footer' not in result
        assert 'sidebar' not in result
        assert 'script' not in result
        assert 'style' not in result
        assert 'comments' not in result
    
    def test_clean_content_unwraps_disallowed_tags(self):
        """Test that disallowed tags are unwrapped but content preserved"""
        html = """
        <div>
            <p>Allowed paragraph</p>
            <span>Content in span tag</span>
            <section>Content in section tag</section>
            <article>Content in article tag</article>
        </div>
        """
        content_div = BeautifulSoup(html, 'html.parser').find('div')
        
        result = self.parser.clean_content_for_publishing(content_div)
        
        # Should keep allowed paragraph tag
        assert '<p>Allowed paragraph</p>' in result
        # Should unwrap disallowed tags but keep content
        assert 'Content in span tag' in result
        assert 'Content in section tag' in result
        assert 'Content in article tag' in result
        # Should not contain the disallowed tag names
        assert '<span>' not in result
        assert '<section>' not in result
        assert '<article>' not in result
    
    def test_clean_content_preserves_allowed_tags(self):
        """Test that allowed tags are preserved"""
        allowed_tags_html = """
        <div>
            <a href="link">Link</a>
            <b>Bold</b>
            <i>Italic</i>
            <em>Emphasis</em>
            <strong>Strong</strong>
            <u>Underline</u>
            <s>Strikethrough</s>
            <blockquote>Quote</blockquote>
            <code>Code</code>
            <pre>Preformatted</pre>
            <p>Paragraph</p>
            <ul><li>List item</li></ul>
            <ol><li>Ordered item</li></ol>
            <br>
            <hr>
            <img src="image.jpg">
        </div>
        """
        content_div = BeautifulSoup(allowed_tags_html, 'html.parser').find('div')
        
        result = self.parser.clean_content_for_publishing(content_div)
        
        # All these tags should be preserved
        preserved_tags = ['<a', '<b>', '<i>', '<em>', '<strong>', '<u>', '<s>', 
                         '<blockquote>', '<code>', '<pre>', '<p>', '<ul>', '<ol>', 
                         '<li>', '<br', '<hr', '<img']
        
        for tag in preserved_tags:
            assert tag in result


class TestReviewParserExtractAuthors:
    """Test the _extract_authors method"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.parser = ReviewParser("https://example.com")
    
    def test_extract_authors_without_by_prefix(self):
        """Test author extraction without 'by' prefix (normal case)"""
        html = """
        <div class="bpf-content">
            <h2>Desmund Hui and Griffith Jones</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_authors(soup)
        assert result == ['Desmund Hui', 'Griffith Jones']
    
    def test_extract_authors_with_by_prefix_lowercase(self):
        """Test author extraction with 'by' prefix (lowercase)"""
        html = """
        <div class="bpf-content">
            <h2>by John Doe and Jane Smith</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_authors(soup)
        assert result == ['John Doe', 'Jane Smith']
    
    def test_extract_authors_with_by_prefix_capitalized(self):
        """Test author extraction with 'By' prefix (capitalized)"""
        html = """
        <div class="bpf-content">
            <h2>By Alice Cooper and Bob Wilson</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_authors(soup)
        assert result == ['Alice Cooper', 'Bob Wilson']
    
    def test_extract_authors_single_author(self):
        """Test author extraction with single author"""
        html = """
        <div class="bpf-content">
            <h2>John Doe</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_authors(soup)
        assert result == ['John Doe']
    
    def test_extract_authors_no_byline_element(self):
        """Test author extraction when no byline element exists"""
        html = "<html><body><p>No authors here</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_authors(soup)
        assert result == []
    
    def test_extract_authors_preserves_case(self):
        """Test that author names preserve original case"""
        html = """
        <div class="bpf-content">
            <h2>John DOE and jane smith</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_authors(soup)
        assert result == ['John DOE', 'jane smith']
    
    def test_extract_authors_multiple_separators(self):
        """Test author extraction with various separators"""
        html = """
        <div class="bpf-content">
            <h2>John Doe, Jane Smith and Bob Wilson</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_authors(soup)
        assert result == ['John Doe', 'Jane Smith', 'Bob Wilson']
    
    def test_extract_authors_filters_empty_strings(self):
        """Test that empty strings are filtered out"""
        html = """
        <div class="bpf-content">
            <h2>John Doe,  , Jane Smith</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_authors(soup)
        assert result == ['John Doe', 'Jane Smith']


class TestReviewParserExtractDate:
    """Test the _extract_date method"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.parser = ReviewParser("https://example.com")
    
    def test_extract_date_single_month(self):
        """Test date extraction for single month"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Platypus Review 173 | February 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_date(soup)
        assert result == "February 2025"
    
    def test_extract_date_multiple_months(self):
        """Test date extraction for multiple months"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Platypus Review 178 | July–August 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_date(soup)
        assert result == "July–August 2025"
    
    def test_extract_date_no_pipe_separator(self):
        """Test date extraction when no pipe separator exists"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Platypus Review 173 February 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_date(soup)
        assert result == ""  # Should fallback to empty string
    
    def test_extract_date_fallback_to_time_element(self):
        """Test date extraction fallback to time element"""
        html = """
        <html>
            <body>
                <time datetime="2025-02-01">February 1, 2025</time>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_date(soup)
        assert result == "2025-02-01"
    
    def test_extract_date_fallback_to_date_class(self):
        """Test date extraction fallback to date class"""
        html = """
        <html>
            <body>
                <span class="date">March 2025</span>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        with patch.object(self.parser, 'clean_text') as mock_clean:
            mock_clean.return_value = "March 2025"
            result = self.parser._extract_date(soup)
            assert result == "March 2025"
    
    def test_extract_date_no_date_found(self):
        """Test date extraction when no date is found"""
        html = "<html><body><p>No date here</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_date(soup)
        assert result == ""


class TestReviewParserExtractId:
    """Test the _extract_id method"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.parser = ReviewParser("https://example.com")
    
    def test_extract_id_with_space(self):
        """Test ID extraction with space between Review and number"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Platypus Review 173 | February 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_id(soup)
        assert result == 173
    
    def test_extract_id_without_space(self):
        """Test ID extraction without space between Review and number"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Platypus Review173 | February 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_id(soup)
        assert result == 173
    
    def test_extract_id_multiple_spaces(self):
        """Test ID extraction with multiple spaces"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Platypus Review   178 | July 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_id(soup)
        assert result == 178
    
    def test_extract_id_no_container(self):
        """Test ID extraction when container doesn't exist"""
        html = "<html><body><p>No review info here</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_id(soup)
        # Should fallback to hash-based ID
        expected = hash(self.parser.base_url) % 1000000
        assert result == expected
    
    def test_extract_id_no_match(self):
        """Test ID extraction when pattern doesn't match"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Some other text | February 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = self.parser._extract_id(soup)
        # Should fallback to hash-based ID
        expected = hash(self.parser.base_url) % 1000000
        assert result == expected
    
    def test_extract_id_regex_pattern(self):
        """Test that the regex pattern works correctly"""
        pattern = r'Platypus Review\s*(\d+)'
        
        # Test cases
        test_cases = [
            ("Platypus Review 173", "173"),
            ("Platypus Review173", "173"),
            ("Platypus Review  178", "178"),
            ("Platypus Review\t173", "173"),
        ]
        
        for text, expected_id in test_cases:
            match = re.search(pattern, text)
            assert match is not None
            assert match.group(1) == expected_id
        
        # Negative test cases
        negative_cases = [
            "platypus review 173",  # Case sensitive
            "Review 173",           # Missing "Platypus"
            "Platypus Review ABC",  # No digits
        ]
        
        for text in negative_cases:
            match = re.search(pattern, text)
            assert match is None


class TestReviewParserAbstractMethodImplementation:
    """Test that ReviewParser properly implements all abstract methods"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.parser = ReviewParser("https://example.com")
    
    def test_implements_all_abstract_methods(self):
        """Test that all abstract methods are implemented"""
        abstract_methods = [
            'parse_listing_page',
            'parse_content_page',
            'extract_title', 
            'extract_content',
            'extract_metadata',
            'clean_content_for_publishing'
        ]
        
        for method_name in abstract_methods:
            assert hasattr(self.parser, method_name)
            assert callable(getattr(self.parser, method_name))
    
    def test_methods_return_correct_types(self):
        """Test that methods return expected types"""
        # Test with minimal HTML
        html = "<html><body><h1>Test</h1></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        # parse_listing_page should return list
        result = self.parser.parse_listing_page(html)
        assert isinstance(result, list)
        
        # extract_title should return string
        result = self.parser.extract_title(soup)
        assert isinstance(result, str)
        
        # extract_metadata should return dict
        with patch.object(self.parser, '_extract_authors') as mock_authors, \
             patch.object(self.parser, '_extract_date') as mock_date, \
             patch.object(self.parser, '_extract_id') as mock_id:
            
            mock_authors.return_value = []
            mock_date.return_value = ""
            mock_id.return_value = 123
            
            result = self.parser.extract_metadata(soup)
            assert isinstance(result, dict)
        
        # clean_content_for_publishing should return string
        result = self.parser.clean_content_for_publishing(soup)
        assert isinstance(result, str)
