import pytest
from bs4 import BeautifulSoup
from src.scraping.review_parser import ReviewParser


class TestReviewParserIntegration:
    """Integration tests for ReviewParser using real HTML samples"""

    # Example HTML for a listing page (simulated Platypus Review structure)
    LISTING_HTML = """
    <html>
      <body>
        <h4><a href="https://platypus1917.org/2025/01/01/article1/">Article 1</a></h4>
        <h4><a href="https://platypus1917.org/2024/12/15/article2/">Article 2</a></h4>
        <h4><a href="https://example.com/external/">External Link</a></h4>
        <h4><a href="https://platypus1917.org/about/">About Page</a></h4>
      </body>
    </html>
    """

    # Example HTML for a content page (simulated Platypus Review structure)
    CONTENT_HTML = """
    <html>
      <body>
        <h1>Marxism and the Left Today</h1>
        <div class="dc-page-seo-wrapper">
          <p>This is the main content of the article discussing Marxism.</p>
          <blockquote>
            "The critique of political economy is the foundation of Marxist theory."
          </blockquote>
          <div>
            <strong>Key points:</strong>
            <ul>
              <li>Historical materialism</li>
              <li>Class struggle</li>
            </ul>
          </div>
          <script>console.log('This should be removed');</script>
          <nav>Navigation should be removed</nav>
        </div>
        <div class="bpf-content">
          <h2>by John Doe and Jane Smith</h2>
          <p class="has-text-align-right">Platypus Review 173 | February 2025</p>
        </div>
      </body>
    </html>
    """

    def setup_method(self):
        """Set up test fixtures for each test method"""
        self.parser = ReviewParser(base_url="https://platypus1917.org/platypus-review/")

    def test_parse_listing_page_integration(self):
        """Integration test: parse_listing_page extracts correct URLs from real HTML"""
        urls = self.parser.parse_listing_page(self.LISTING_HTML)
        
        # Should only extract Platypus articles from 20xx years
        expected_urls = [
            "https://platypus1917.org/2025/01/01/article1/",
            "https://platypus1917.org/2024/12/15/article2/"
        ]
        assert urls == expected_urls

    def test_parse_content_page_integration(self):
        """Integration test: parse_content_page extracts all fields from real HTML"""
        url = "https://platypus1917.org/2025/01/01/marxism-left-today/"
        result = self.parser.parse_content_page(self.CONTENT_HTML, url)

        # Verify all extracted fields
        assert result["title"] == "Marxism and the Left Today"
        assert "main content of the article discussing Marxism" in result["content"]
        assert result["original_url"] == url
        assert result["authors"] == ["John Doe", "Jane Smith"]
        assert result["published_date"] == "February 2025"
        # Note: review_id is extracted separately via extract_review_id method    def test_extract_metadata_integration(self):
        """Integration test: extract_metadata returns correct dict from real HTML"""
        soup = BeautifulSoup(self.CONTENT_HTML, "html.parser")
        metadata = self.parser.extract_metadata(soup)

        expected_metadata = {
            "authors": ["John Doe", "Jane Smith"],
            "published_date": "February 2025"
        }
        assert metadata == expected_metadata

    def test_extract_review_id_integration(self):
        """Integration test: extract_review_id works with real HTML"""
        # Test with span.selected format
        html = '<html><body><span class="selected">Archive for category Issue #173</span></body></html>'
        review_id = self.parser.extract_review_id(html)
        assert review_id == 173

    def test_extract_title_integration(self):
        """Integration test: extract_title returns correct title from real HTML"""
        soup = BeautifulSoup(self.CONTENT_HTML, "html.parser")
        title = self.parser.extract_title(soup)
        assert title == "Marxism and the Left Today"

    def test_extract_content_integration(self):
        """Integration test: extract_content returns cleaned HTML from real HTML"""
        soup = BeautifulSoup(self.CONTENT_HTML, "html.parser")
        content = self.parser.extract_content(soup)
        
        # Should contain main content
        assert "main content of the article discussing Marxism" in content
        assert "The critique of political economy" in content
        assert "Historical materialism" in content
        
        # Should preserve allowed HTML tags
        assert "<blockquote>" in content
        assert "<strong>" in content
        assert "<ul>" in content
        assert "<li>" in content
        
        # Should remove unwanted elements
        assert "console.log" not in content
        assert "Navigation should be removed" not in content


class TestReviewParserEdgeCasesIntegration:
    """Integration tests for ReviewParser edge cases with real-like HTML"""

    def setup_method(self):
        """Set up test fixtures for each test method"""
        self.parser = ReviewParser(base_url="https://platypus1917.org/platypus-review/")

    def test_content_without_wrapper_integration(self):
        """Integration test: content extraction when dc-page-seo-wrapper is missing"""
        html_without_wrapper = """
        <html>
          <body>
            <h1>Article Without Wrapper</h1>
            <p>This content is not wrapped in dc-page-seo-wrapper.</p>
            <div class="bpf-content">
              <h2>Single Author</h2>
              <p class="has-text-align-right">Platypus Review 175 | April 2025</p>
            </div>
          </body>
        </html>
        """

        result = self.parser.parse_content_page(html_without_wrapper, "test-url")

        assert result["title"] == "Article Without Wrapper"
        assert "not wrapped in dc-page-seo-wrapper" in result["content"]
        assert result["authors"] == ["Single Author"]
        # Note: review_id is extracted separately via extract_review_id method    def test_authors_with_different_formats_integration(self):
        """Integration test: author extraction with various formatting"""
        html_variants = [
            # No "by" prefix
            """
            <div class="bpf-content">
              <h2>Alice Cooper and Bob Wilson</h2>
            </div>
            """,
            # "By" capitalized
            """
            <div class="bpf-content">
              <h2>By Charlie Brown</h2>
            </div>
            """,
            # Multiple separators
            """
            <div class="bpf-content">
              <h2>David Lee, Emma Stone and Frank Ocean</h2>
            </div>
            """
        ]
        
        expected_authors = [
            ["Alice Cooper", "Bob Wilson"],
            ["Charlie Brown"],
            ["David Lee", "Emma Stone", "Frank Ocean"]
        ]
        
        for html, expected in zip(html_variants, expected_authors):
            soup = BeautifulSoup(html, "html.parser")
            authors = self.parser._extract_authors(soup)
            assert authors == expected

    def test_date_extraction_variants_integration(self):
        """Integration test: date extraction with different formats"""
        date_variants = [
            # Single month
            ('<p class="has-text-align-right">Platypus Review 180 | March 2025</p>', "March 2025"),
            # Multiple months with em dash
            ('<p class="has-text-align-right">Platypus Review 181 | July–August 2025</p>', "July–August 2025"),
            # Fallback to time element
            ('<time datetime="2025-05-01">May 1, 2025</time>', "2025-05-01"),
        ]
        
        for html_snippet, expected_date in date_variants:
            html = f'<div class="bpf-content">{html_snippet}</div>'
            soup = BeautifulSoup(html, "html.parser")
            date = self.parser._extract_date(soup)
            assert date == expected_date

    def test_review_id_extraction_variants_integration(self):
        """Integration test: review ID extraction with span.selected format"""
        id_variants = [
            # Normal format
            ("Archive for category Issue #173", 173),
            # Different issue numbers  
            ("Archive for category Issue #178", 178),
            ("Archive for category Issue #180", 180),
            ("Archive for category Issue #001", 1),
        ]

        for text, expected_id in id_variants:
            # Test the extract_review_id method with span.selected
            html = f'<html><body><span class="selected">{text}</span></body></html>'
            review_id = self.parser.extract_review_id(html)
            assert review_id == expected_id

    def test_review_id_extraction_url_fallback_integration(self):
        """Integration test: review ID extraction from URL when span fails"""
        # Set parser base_url to test URL fallback
        parser = ReviewParser("https://platypus1917.org/category/pr/issue-175/")
        
        # HTML without span.selected should fallback to URL
        html = '<html><body><p>No issue span here</p></body></html>'
        review_id = parser.extract_review_id(html)
        assert review_id == 175
class TestReviewParserComplexContentIntegration:
    """Integration tests for ReviewParser with complex, realistic HTML content"""

    def setup_method(self):
        """Set up test fixtures for each test method"""
        self.parser = ReviewParser(base_url="https://platypus1917.org/platypus-review/")

    def test_complex_article_structure_integration(self):
        """Integration test: full article with complex HTML structure"""
        complex_html = """
        <html>
          <head>
            <title>Page Title</title>
          </head>
          <body>
            <header>Site Header</header>
            <nav>Site Navigation</nav>
            
            <main>
              <h1>The Crisis of Marxism in the 21st Century</h1>
              
              <div class="dc-page-seo-wrapper">
                <p>Introduction paragraph with <em>emphasis</em> and <strong>strong text</strong>.</p>
                
                <blockquote cite="https://example.com">
                  "The philosophers have only interpreted the world in various ways; 
                  the point is to change it." — Karl Marx
                </blockquote>
                
                <h2>Historical Context</h2>
                <p>The development of Marxist thought has undergone several phases:</p>
                
                <ol>
                  <li>Classical Marxism (1840s-1880s)</li>
                  <li>Second International period (1889-1914)</li>
                  <li>Revolutionary period (1917-1920s)</li>
                </ol>
                
                <h3>Key Theoretical Developments</h3>
                <ul>
                  <li><a href="/article/dialectical-materialism">Dialectical materialism</a></li>
                  <li><a href="/article/historical-materialism">Historical materialism</a></li>
                  <li><a href="/article/critique-political-economy">Critique of political economy</a></li>
                </ul>
                
                <p>Modern interpretations must grapple with <code>contemporary conditions</code>.</p>
                
                <pre>
                # Example of formatted code or text
                class Revolution:
                    def __init__(self, conditions):
                        self.material_conditions = conditions
                </pre>
                
                <hr>
                
                <p>Conclusion with <u>underlined</u> and <s>strikethrough</s> text.</p>
                
                <!-- Comment that should be ignored -->
                <script>
                  // This script should be removed
                  console.log("tracking code");
                </script>
                
                <div class="sidebar">
                  <p>Sidebar content that should be removed</p>
                </div>
                
                <footer>Article footer that should be removed</footer>
              </div>
              
              <div class="bpf-content">
                <h2>Desmund Hui and Griffith Jones</h2>
                <p class="has-text-align-right">Platypus Review 174 | March–April 2025</p>
              </div>
            </main>
            
            <footer>Site Footer</footer>
          </body>
        </html>
        """
        
        url = "https://platypus1917.org/2025/03/15/crisis-marxism-21st-century/"
        result = self.parser.parse_content_page(complex_html, url)
        
        # Verify title extraction
        assert result["title"] == "The Crisis of Marxism in the 21st Century"
        
        # Verify content preservation and cleaning
        content = result["content"]
        
        # Should preserve main content
        assert "Introduction paragraph" in content
        assert "Karl Marx" in content
        assert "Historical Context" in content
        assert "Classical Marxism" in content
        
        # Should preserve allowed HTML tags
        assert "<em>emphasis</em>" in content
        assert "<strong>strong text</strong>" in content
        assert "<blockquote" in content
        assert "<ol>" in content and "<li>" in content
        assert "<ul>" in content
        assert "<a href=" in content
        assert "<code>" in content
        assert "<pre>" in content
        assert "<hr" in content
        assert "<u>underlined</u>" in content
        assert "<s>strikethrough</s>" in content
        
        # Should remove unwanted elements
        assert "tracking code" not in content
        assert "Sidebar content" not in content
        assert "Article footer" not in content
        assert "Site Header" not in content
        assert "Site Navigation" not in content
        assert "Site Footer" not in content
        assert "<script>" not in content
        assert "<footer>" not in content
        assert "sidebar" not in content.lower()
        
        # Verify metadata extraction
        assert result["authors"] == ["Desmund Hui", "Griffith Jones"]
        assert result["published_date"] == "March–April 2025"
        # Note: review_id is extracted separately via extract_review_id method
        assert result["original_url"] == url

    def test_minimal_article_structure_integration(self):
        """Integration test: minimal article with basic required elements"""
        minimal_html = """
        <html>
          <body>
            <h1>Brief Article</h1>
            <p>Short content.</p>
            <div class="bpf-content">
              <h2>Anonymous</h2>
              <p class="has-text-align-right">Platypus Review 176 | May 2025</p>
            </div>
          </body>
        </html>
        """
        
        url = "https://platypus1917.org/2025/05/01/brief-article/"
        result = self.parser.parse_content_page(minimal_html, url)
        
        assert result["title"] == "Brief Article"
        assert "Short content." in result["content"]
        assert result["authors"] == ["Anonymous"]
        assert result["published_date"] == "May 2025"
        # Note: review_id is extracted separately via extract_review_id method
        assert result["original_url"] == url
