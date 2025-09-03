import pytest
import re
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup

from src.scraping.parser import Parser
from src.scraping.review_parser import ReviewParser
from src.scraping.constants import ALLOWED_TAGS, IRRELEVANT_INFO_TAGS

@pytest.fixture
def review_parser():
    return ReviewParser("https://platypus1917.org/platypus-review/")

@pytest.fixture
def simple_parser():
    return ReviewParser("https://example.com")

class TestReviewParser:
    """Test the ReviewParser concrete implementation"""
    
    def test_init(self, review_parser):
        """Test ReviewParser initialization"""
        assert review_parser.base_url == "https://platypus1917.org/platypus-review/"
        assert isinstance(review_parser, Parser)
    
    @pytest.mark.parametrize(
        "html, expected_urls, test_description",
        [
            # Successful parsing with matching links (original success case)
            (
                """
                <html>
                    <body>
                        <h4><a href="https://platypus1917.org/2025/01/01/article1/">Article 1</a></h4>
                        <h4><a href="https://platypus1917.org/2024/12/15/article2/">Article 2</a></h4>
                        <h4><a href="https://example.com/external/">External Link</a></h4>
                        <h4><a href="/relative/link/">Relative Link</a></h4>
                    </body>
                </html>
                """,
                [
                    "https://platypus1917.org/2025/01/01/article1/",
                    "https://platypus1917.org/2024/12/15/article2/"
                ],
                "success_case"
            ),
            # Empty HTML (original empty case)
            (
                "<html><body></body></html>",
                [],
                "empty_html"
            ),
            # No matching links (original no matching case)
            (
                """
                <html>
                    <body>
                        <h4><a href="https://other-site.com/article/">Other Site</a></h4>
                        <h4><a href="https://platypus1917.org/about/">About Page</a></h4>
                    </body>
                </html>
                """,
                [],
                "no_matching_links"
            ),
            # HTML with matching absolute URLs
            (
                """
                <html><body>
                    <h4><a href="https://platypus1917.org/2025/01/article1/">Article 1</a></h4>
                    <h4><a href="https://platypus1917.org/2024/12/article2/">Article 2</a></h4>
                </body></html>
                """,
                ["https://platypus1917.org/2025/01/article1/", "https://platypus1917.org/2024/12/article2/"],
                "absolute_urls"
            ),
            # HTML with matching relative URLs
            (
                """
                <html><body>
                    <h4><a href="/2025/01/article1/">Article 1</a></h4>
                    <h4><a href="/2024/12/article2/">Article 2</a></h4>
                </body></html>
                """,
                ["https://platypus1917.org/2025/01/article1/", "https://platypus1917.org/2024/12/article2/"],
                "relative_urls"
            ),
            # HTML with mixed URLs (some matching, some not)
            (
                """
                <html><body>
                    <h4><a href="https://platypus1917.org/2025/01/article1/">Article 1</a></h4>
                    <h4><a href="https://external.com/article/">External</a></h4>
                    <h4><a href="/2024/12/article2/">Article 2</a></h4>
                    <h4><a href="https://platypus1917.org/about/">About Page</a></h4>
                </body></html>
                """,
                # Order matches actual implementation: relative URLs first, then absolute URLs
                ["https://platypus1917.org/2024/12/article2/", "https://platypus1917.org/2025/01/article1/"],
                "mixed_urls"
            ),
        ]
    )
    def test_parse_listing_page_scenarios(self, review_parser, html, expected_urls, test_description):
        """Test parse_listing_page with various HTML scenarios"""
        result = review_parser.parse_listing_page(html)
        assert result == expected_urls
    
    def test_parse_content_page_success(self, review_parser):
        """Test successful parsing of content page"""
        url = "https://platypus1917.org/2025/01/01/test-article/"
        
        with patch.object(review_parser, 'extract_title') as mock_title, \
             patch.object(review_parser, 'extract_content') as mock_content, \
             patch.object(review_parser, 'extract_metadata') as mock_metadata:
            
            mock_title.return_value = "Test Article"
            mock_content.return_value = "<p>Test content</p>"
            mock_metadata.return_value = {
                'authors': ['John Doe'],
                'published_date': 'January 2025',
                'review_id': 173
            }
            
            result = review_parser.parse_content_page("<html>test</html>", url)
            
            expected = {
                'title': 'Test Article',
                'content': '<p>Test content</p>',
                'original_url': url,
                'authors': ['John Doe'],
                'published_date': 'January 2025',
                'review_id': 173
            }
            
            assert result == expected
    
    @pytest.mark.parametrize(
        "html, expected_title", 
        [
            ("<html><body><h1>  Test Article Title  </h1></body></html>", "Test Article Title"), # normal title
            ("<html><body><h2>Not a title</h2></body></html>", "Untitled") # title_no_h1
        ]
    )
    def test_extract_title(self, review_parser, html, expected_title):
        """Test extract_title with various scenarios"""
        soup = BeautifulSoup(html, 'html.parser')
        result = review_parser.extract_title(soup)
        assert result == expected_title
        
    def test_extract_content_with_wrapper(self, review_parser):
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
        
        with patch.object(review_parser, 'clean_content_for_publishing') as mock_clean:
            mock_clean.return_value = "cleaned content"
            result = review_parser.extract_content(soup)
            
            # Should pass the dc-page-seo-wrapper div to cleaning
            mock_clean.assert_called_once()
            args = mock_clean.call_args[0]
            assert args[0].get('class') == ['dc-page-seo-wrapper']
            assert result == "cleaned content"
    
    def test_extract_content_fallback_to_full_soup(self, review_parser):
        """Test content extraction fallback when no wrapper found"""
        html = "<html><body><p>Content without wrapper</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        with patch.object(review_parser, 'clean_content_for_publishing') as mock_clean:
            mock_clean.return_value = "cleaned content"
            result = review_parser.extract_content(soup)
            
            # Should pass the entire soup to cleaning
            mock_clean.assert_called_once()
            args = mock_clean.call_args[0]
            assert args[0].name == "[document]"  # BeautifulSoup document
            assert result == "cleaned content"
    
    def test_extract_metadata_success(self, review_parser):
        """Test successful metadata extraction"""
        soup = Mock()
        
        with patch.object(review_parser, '_extract_authors') as mock_authors, \
             patch.object(review_parser, '_extract_date') as mock_date, \
             patch.object(review_parser, '_extract_id') as mock_id:
            
            mock_authors.return_value = ['Author 1', 'Author 2']
            mock_date.return_value = 'February 2025'
            mock_id.return_value = 173
            
            result = review_parser.extract_metadata(soup)
            
            expected = {
                'authors': ['Author 1', 'Author 2'],
                'published_date': 'February 2025',
                'review_id': 173
            }
            
            assert result == expected
            mock_authors.assert_called_once_with(soup)
            mock_date.assert_called_once_with(soup)
            mock_id.assert_called_once_with(soup)

    @pytest.mark.parametrize(
        "title_html, expected_title",
        [
            ("<h1>Clean Title</h1>", "Clean Title"),
            ("<h1>  Title with spaces  </h1>", "Title with spaces"),
            ("<h1>Title\nwith\nnewlines</h1>", "Title with newlines"),
            ("<h1>Title\t\twith\t\ttabs</h1>", "Title with tabs"),
            ("<h1></h1>", ""),
            ("<h2>Not an h1</h2>", "Untitled"),  # No h1 tag
            ("", "Untitled"),  # No tags at all
        ]
    )
    def test_extract_title_scenarios(self, review_parser, title_html, expected_title):
        """Test extract_title with various title scenarios"""
        html = f"<html><body>{title_html}</body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        result = review_parser.extract_title(soup)
        assert result == expected_title

    @pytest.mark.parametrize(
        "href, expected_url",
        [
            # Absolute URLs (no normalization needed)
            ("https://platypus1917.org/2025/01/article/", "https://platypus1917.org/2025/01/article/"),
            ("https://external.com/article/", "https://external.com/article/"),
            # Relative URLs starting with / (normalization needed)
            ("/2025/01/article/", "https://platypus1917.org/2025/01/article/"),
            ("/2024/12/test/", "https://platypus1917.org/2024/12/test/"),
            # URLs with whitespace - not normalized because they don't start with "/"
            ("  /2025/01/article/  ", "  /2025/01/article/  "),
        ]
    )
    def test_extract_link_positive_cases(self, review_parser, href, expected_url):
        """Test extract_link with valid URLs that should be successfully extracted"""
        html = f'<a href="{href}">Article</a>'
        link = BeautifulSoup(html, 'html.parser').find('a')
        
        result = review_parser.extract_link(link)
        assert result == expected_url

    @pytest.mark.parametrize(
        "href, expected_url",
        [
            # Edge cases that are NOT normalized (don't start with /)
            ("../parent/directory", "../parent/directory"),
            ("?query=param", "?query=param"),
            ("#anchor", "#anchor"),
        ]
    )
    def test_extract_link_edge_cases_not_normalized(self, review_parser, href, expected_url):
        """Test extract_link with URLs that are not normalized by current implementation"""
        html = f'<a href="{href}">Article</a>'
        link = BeautifulSoup(html, 'html.parser').find('a')
        
        result = review_parser.extract_link(link)
        assert result == expected_url

    @pytest.mark.parametrize(
        "href, html_template",
        [
            # Empty href
            ("", '<a href="">Article with empty href</a>'),
            # No href attribute
            (None, '<a>Article without href</a>'),
        ]
    )
    def test_extract_link_negative_cases(self, review_parser, href, html_template):
        """Test extract_link with invalid cases that should return None"""
        link = BeautifulSoup(html_template, 'html.parser').find('a')
        
        result = review_parser.extract_link(link)
        assert result is None

    def test_extract_link_with_normalize_url_mock(self, review_parser):
        """Test that normalize_url is called with correct parameters"""
        html = '<a href="/test/path">Article</a>'
        link = BeautifulSoup(html, 'html.parser').find('a')
        
        with patch.object(review_parser, 'normalize_url') as mock_normalize:
            mock_normalize.return_value = "https://normalized.url"
            
            result = review_parser.extract_link(link)
            
            mock_normalize.assert_called_once_with("/test/path", review_parser.base_url)
            assert result == "https://normalized.url"


class TestReviewParserCleanContent:
    """Test the clean_content_for_publishing method"""
    
    def test_clean_content_preserves_allowed_tags(self, simple_parser):
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
        
        result = simple_parser.clean_content_for_publishing(content_div)
        
        # All these tags should be preserved
        preserved_tags = ['<a', '<b>', '<i>', '<em>', '<strong>', '<u>', '<s>', 
                         '<blockquote>', '<code>', '<pre>', '<p>', '<ul>', '<ol>', 
                         '<li>', '<br', '<hr', '<img']
        
        for tag in preserved_tags:
            assert tag in result

    def test_remove_unwanted_elements_subfunction(self, simple_parser):
        """Test the _remove_unwanted_elements subfunction"""
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
        soup = BeautifulSoup(html, 'html.parser')
        
        simple_parser._remove_unwanted_elements(soup)
        
        result = str(soup)
        
        # Should keep the paragraph
        assert '<p>Keep this paragraph</p>' in result
        # Should remove unwanted elements
        assert 'nav' not in result
        assert 'footer' not in result
        assert 'sidebar' not in result
        assert 'script' not in result
        assert 'style' not in result
        assert 'comments' not in result

    def test_clean_disallowed_tags_subfunction(self, simple_parser):
        """Test the _clean_disallowed_tags subfunction"""
        html = """
        <div>
            <p>Allowed paragraph</p>
            <span>Content in span tag</span>
            <section>Content in section tag</section>
            <article>Content in article tag</article>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        simple_parser._clean_disallowed_tags(soup)
        
        result = str(soup)
        
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


class TestReviewParserExtractAuthors:
    """Test the _extract_authors method"""
    
    def test_extract_authors_without_by_prefix(self, simple_parser):
        """Test author extraction without 'by' prefix (normal case)"""
        html = """
        <div class="bpf-content">
            <h2>Desmund Hui and Griffith Jones</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_authors(soup)
        assert result == ['Desmund Hui', 'Griffith Jones']
    
    def test_extract_authors_with_by_prefix_lowercase(self, simple_parser):
        """Test author extraction with 'by' prefix (lowercase)"""
        html = """
        <div class="bpf-content">
            <h2>by John Doe and Jane Smith</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_authors(soup)
        assert result == ['John Doe', 'Jane Smith']
    
    def test_extract_authors_with_by_prefix_capitalized(self, simple_parser):
        """Test author extraction with 'By' prefix (capitalized)"""
        html = """
        <div class="bpf-content">
            <h2>By Alice Cooper and Bob Wilson</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_authors(soup)
        assert result == ['Alice Cooper', 'Bob Wilson']
    
    def test_extract_authors_single_author(self, simple_parser):
        """Test author extraction with single author"""
        html = """
        <div class="bpf-content">
            <h2>John Doe</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_authors(soup)
        assert result == ['John Doe']
    
    def test_extract_authors_no_byline_element(self, simple_parser):
        """Test author extraction when no byline element exists"""
        html = "<html><body><p>No authors here</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_authors(soup)
        assert result == []
    
    def test_extract_authors_preserves_case(self, simple_parser):
        """Test that author names preserve original case"""
        html = """
        <div class="bpf-content">
            <h2>John DOE and jane smith</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_authors(soup)
        assert result == ['John DOE', 'jane smith']
    
    def test_extract_authors_multiple_separators(self, simple_parser):
        """Test author extraction with various separators"""
        html = """
        <div class="bpf-content">
            <h2>John Doe, Jane Smith and Bob Wilson</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_authors(soup)
        assert result == ['John Doe', 'Jane Smith', 'Bob Wilson']
    
    def test_extract_authors_filters_empty_strings(self, simple_parser):
        """Test that empty strings are filtered out"""
        html = """
        <div class="bpf-content">
            <h2>John Doe,  , Jane Smith</h2>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_authors(soup)
        assert result == ['John Doe', 'Jane Smith']


class TestReviewParserExtractDate:
    """Test the _extract_date method"""
    
    def test_extract_date_single_month(self, simple_parser):
        """Test date extraction for single month"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Platypus Review 173 | February 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_date(soup)
        assert result == "February 2025"
    
    def test_extract_date_multiple_months(self, simple_parser):
        """Test date extraction for multiple months"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Platypus Review 178 | July–August 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_date(soup)
        assert result == "July–August 2025"
    
    def test_extract_date_no_pipe_separator(self, simple_parser):
        """Test date extraction when no pipe separator exists"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Platypus Review 173 February 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_date(soup)
        assert result == ""  # Should fallback to empty string
    
    def test_extract_date_fallback_to_time_element(self, simple_parser):
        """Test date extraction fallback to time element"""
        html = """
        <html>
            <body>
                <time datetime="2025-02-01">February 1, 2025</time>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_date(soup)
        assert result == "2025-02-01"
    
    def test_extract_date_fallback_to_date_class(self, simple_parser):
        """Test date extraction fallback to date class"""
        html = """
        <html>
            <body>
                <span class="date">March 2025</span>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        with patch.object(simple_parser, 'clean_text') as mock_clean:
            mock_clean.return_value = "March 2025"
            result = simple_parser._extract_date(soup)
            assert result == "March 2025"
    
    def test_extract_date_no_date_found(self, simple_parser):
        """Test date extraction when no date is found"""
        html = "<html><body><p>No date here</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_date(soup)
        assert result == ""


class TestReviewParserExtractId:
    """Test the _extract_id method"""
    
    def test_extract_id_with_space(self, simple_parser):
        """Test ID extraction with space between Review and number"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Platypus Review 173 | February 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_id(soup)
        assert result == 173
    
    def test_extract_id_without_space(self, simple_parser):
        """Test ID extraction without space between Review and number"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Platypus Review173 | February 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_id(soup)
        assert result == 173
    
    def test_extract_id_multiple_spaces(self, simple_parser):
        """Test ID extraction with multiple spaces"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Platypus Review   178 | July 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_id(soup)
        assert result == 178
    
    def test_extract_id_no_container(self, simple_parser):
        """Test ID extraction when container doesn't exist"""
        html = "<html><body><p>No review info here</p></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_id(soup)
        # Should fallback to hash-based ID
        expected = hash(simple_parser.base_url) % 1000000
        assert result == expected
    
    def test_extract_id_no_match(self, simple_parser):
        """Test ID extraction when pattern doesn't match"""
        html = """
        <div class="bpf-content">
            <p class="has-text-align-right">Some other text | February 2025</p>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        result = simple_parser._extract_id(soup)
        # Should fallback to hash-based ID
        expected = hash(simple_parser.base_url) % 1000000
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
    
    def test_implements_all_abstract_methods(self, simple_parser):
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
            assert hasattr(simple_parser, method_name)
            assert callable(getattr(simple_parser, method_name))
    
    def test_methods_return_correct_types(self, simple_parser):
        """Test that methods return expected types"""
        # Test with minimal HTML
        html = "<html><body><h1>Test</h1></body></html>"
        soup = BeautifulSoup(html, 'html.parser')
        
        # parse_listing_page should return list
        result = simple_parser.parse_listing_page(html)
        assert isinstance(result, list)
        
        # extract_title should return string
        result = simple_parser.extract_title(soup)
        assert isinstance(result, str)
        
        # extract_metadata should return dict
        with patch.object(simple_parser, '_extract_authors') as mock_authors, \
             patch.object(simple_parser, '_extract_date') as mock_date, \
             patch.object(simple_parser, '_extract_id') as mock_id:
            
            mock_authors.return_value = []
            mock_date.return_value = ""
            mock_id.return_value = 123
            
            result = simple_parser.extract_metadata(soup)
            assert isinstance(result, dict)
        
        # clean_content_for_publishing should return string
        result = simple_parser.clean_content_for_publishing(soup)
        assert isinstance(result, str)
