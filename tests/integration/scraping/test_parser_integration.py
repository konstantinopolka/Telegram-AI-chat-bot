import pytest
from bs4 import BeautifulSoup
from src.scraping.parser import Parser
from src.scraping.review_parser import ReviewParser


class TestParserAbstractIntegration:
    """Integration tests for abstract Parser class methods using ReviewParser"""
    
    def setup_method(self):
        """Set up test fixtures for each test method"""
        # Use ReviewParser as concrete implementation of abstract Parser
        self.parser = ReviewParser(base_url="https://platypus1917.org/")
    
    def test_create_soup_integration(self):
        """Integration test: create_soup method with realistic HTML"""
        complex_html = """
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="UTF-8">
            <title>Test Article</title>
          </head>
          <body>
            <article>
              <h1>Test Title</h1>
              <p>Paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
              <ul>
                <li>List item 1</li>
                <li>List item 2</li>
              </ul>
            </article>
          </body>
        </html>
        """
        
        soup = self.parser.create_soup(complex_html)
        
        # Verify BeautifulSoup object creation
        assert isinstance(soup, BeautifulSoup)
        assert soup.name == "[document]"
        
        # Verify parsing accuracy
        assert soup.find('h1').get_text() == "Test Title"
        assert soup.find('strong').get_text() == "bold"
        assert soup.find('em').get_text() == "italic"
        assert len(soup.find_all('li')) == 2
    
    def test_normalize_url_integration(self):
        """Integration test: normalize_url method with various URL types"""
        base_url = "https://platypus1917.org/platypus-review/"
        
        test_cases = [
            # Absolute URLs (should return as-is)
            ("https://example.com/article", "https://example.com/article"),
            ("http://other-site.com/page", "http://other-site.com/page"),
            
            # Relative URLs starting with / (should be normalized)
            ("/2025/01/article/", "https://platypus1917.org/2025/01/article/"),
            ("/about/", "https://platypus1917.org/about/"),
            
            # Relative URLs without / (should return as-is in current implementation)
            ("article/123", "article/123"),
            ("../parent/page", "../parent/page"),
            
            # Edge cases
            ("", ""),
            ("#fragment", "#fragment"),
            ("?query=param", "?query=param"),
        ]
        
        for input_url, expected_output in test_cases:
            result = self.parser.normalize_url(input_url, base_url)
            assert result == expected_output, f"Failed for input: {input_url}"
    
    def test_clean_text_integration(self):
        """Integration test: clean_text method with realistic text content"""
        test_cases = [
            # Whitespace normalization
            ("  Multiple   spaces  between   words  ", "Multiple spaces between words"),
            ("\t\nTabs and\n\nnewlines\t", "Tabs and newlines"),
            
            # Mixed whitespace
            ("  Leading and trailing  ", "Leading and trailing"),
            ("Single word", "Single word"),
            
            # Unicode and special characters
            ("Café naïve résumé", "Café naïve résumé"),
            ("Text with — em dash and – en dash", "Text with — em dash and – en dash"),
            
            # Empty and edge cases
            ("", ""),
            ("   ", ""),
            ("\n\t\r", ""),
        ]
        
        for input_text, expected_output in test_cases:
            result = self.parser.clean_text(input_text)
            assert result == expected_output, f"Failed for input: '{input_text}'"


class TestParserConcreteMethodsIntegration:
    """Integration tests for Parser's concrete utility methods in real scenarios"""
    
    def setup_method(self):
        """Set up test fixtures for each test method"""
        self.parser = ReviewParser(base_url="https://platypus1917.org/")
    
    def test_soup_creation_with_malformed_html_integration(self):
        """Integration test: BeautifulSoup handles malformed HTML gracefully"""
        malformed_html = """
        <html>
          <body>
            <h1>Unclosed title
            <p>Paragraph without closing tag
            <div>
              <span>Nested content</div>
            </span>
          </body>
        <!-- Missing closing html tag
        """
        
        soup = self.parser.create_soup(malformed_html)
        
        # BeautifulSoup should fix the HTML structure
        assert soup.find('h1') is not None
        assert soup.find('p') is not None
        assert soup.find('div') is not None
        assert soup.find('span') is not None
        
        # Should be able to extract text content despite malformed structure
        h1_text = self.parser.clean_text(soup.find('h1').get_text())
        assert "Unclosed title" in h1_text
    
    def test_text_cleaning_with_extracted_content_integration(self):
        """Integration test: clean_text with content extracted from real HTML"""
        html_with_messy_text = """
        <div>
          <h2>   Title with    extra    spaces   </h2>
          <p>
            Paragraph with
            line breaks and   multiple
            
            spaces.
          </p>
          <blockquote>
            "Quote with   
            formatting   issues."
          </blockquote>
        </div>
        """
        
        soup = self.parser.create_soup(html_with_messy_text)
        
        # Extract and clean title
        title_element = soup.find('h2')
        cleaned_title = self.parser.clean_text(title_element.get_text())
        assert cleaned_title == "Title with extra spaces"
        
        # Extract and clean paragraph
        p_element = soup.find('p')
        cleaned_paragraph = self.parser.clean_text(p_element.get_text())
        assert cleaned_paragraph == "Paragraph with line breaks and multiple spaces."
        
        # Extract and clean quote
        quote_element = soup.find('blockquote')
        cleaned_quote = self.parser.clean_text(quote_element.get_text())
        assert cleaned_quote == '"Quote with formatting issues."'
    
    def test_url_normalization_in_link_extraction_integration(self):
        """Integration test: URL normalization during link extraction"""
        html_with_links = """
        <div>
          <a href="/absolute/path">Absolute path link</a>
          <a href="relative/path">Relative path link</a>
          <a href="https://external.com/page">External link</a>
          <a href="#fragment">Fragment link</a>
          <a href="">Empty href</a>
        </div>
        """
        
        soup = self.parser.create_soup(html_with_links)
        base_url = "https://platypus1917.org/base/"
        
        links = soup.find_all('a')
        normalized_urls = []
        
        for link in links:
            href = link.get('href', '')
            normalized_url = self.parser.normalize_url(href, base_url)
            normalized_urls.append(normalized_url)
        
        expected_urls = [
            "https://platypus1917.org/absolute/path",  # Normalized absolute path
            "relative/path",                            # Relative path (as-is)
            "https://external.com/page",               # External URL (as-is)
            "#fragment",                               # Fragment (as-is)
            "",                                        # Empty href (as-is)
        ]
        
        assert normalized_urls == expected_urls


class TestParserWorkflowIntegration:
    """Integration tests for typical Parser workflow patterns"""
    
    def setup_method(self):
        """Set up test fixtures for each test method"""
        self.parser = ReviewParser(base_url="https://platypus1917.org/")
    
    def test_typical_parsing_workflow_integration(self):
        """Integration test: typical workflow of soup creation, extraction, and cleaning"""
        article_html = """
        <html>
          <body>
            <article>
              <h1>   The Future of Socialist Theory   </h1>
              <div class="content">
                <p>
                  This article discusses the    evolution of socialist 
                  thought in the    modern era.
                </p>
                <blockquote>
                  "The   history of all hitherto existing society is the 
                  history of   class struggles."
                </blockquote>
                <ul>
                  <li>   First point   </li>
                  <li>   Second point   </li>
                </ul>
              </div>
              <div class="metadata">
                <p class="author">   by Karl Marx and Friedrich Engels   </p>
                <p class="date">   Published: March 2025   </p>
              </div>
            </article>
          </body>
        </html>
        """
        
        # Step 1: Create soup
        soup = self.parser.create_soup(article_html)
        assert isinstance(soup, BeautifulSoup)
        
        # Step 2: Extract and clean title
        title_element = soup.find('h1')
        title = self.parser.clean_text(title_element.get_text())
        assert title == "The Future of Socialist Theory"
        
        # Step 3: Extract and clean content elements
        content_elements = soup.find('div', class_='content')
        
        paragraph = content_elements.find('p')
        cleaned_paragraph = self.parser.clean_text(paragraph.get_text())
        expected_paragraph = "This article discusses the evolution of socialist thought in the modern era."
        assert cleaned_paragraph == expected_paragraph
        
        quote = content_elements.find('blockquote')
        cleaned_quote = self.parser.clean_text(quote.get_text())
        expected_quote = '"The history of all hitherto existing society is the history of class struggles."'
        assert cleaned_quote == expected_quote
        
        # Step 4: Extract and clean list items
        list_items = content_elements.find_all('li')
        cleaned_items = [self.parser.clean_text(item.get_text()) for item in list_items]
        assert cleaned_items == ["First point", "Second point"]
        
        # Step 5: Extract and clean metadata
        author_element = soup.find('p', class_='author')
        author_text = self.parser.clean_text(author_element.get_text())
        assert author_text == "by Karl Marx and Friedrich Engels"
        
        date_element = soup.find('p', class_='date')
        date_text = self.parser.clean_text(date_element.get_text())
        assert date_text == "Published: March 2025"
    
    def test_error_handling_in_workflow_integration(self):
        """Integration test: parser handles missing elements gracefully"""
        minimal_html = """
        <html>
          <body>
            <p>Just a paragraph, no title or structure.</p>
          </body>
        </html>
        """
        
        soup = self.parser.create_soup(minimal_html)
        
        # Should handle missing title gracefully
        title_element = soup.find('h1')
        if title_element:
            title = self.parser.clean_text(title_element.get_text())
        else:
            title = "No title found"
        
        assert title == "No title found"
        
        # Should extract available content
        paragraph = soup.find('p')
        content = self.parser.clean_text(paragraph.get_text())
        assert content == "Just a paragraph, no title or structure."
        
        # Should handle empty or None gracefully
        empty_text = self.parser.clean_text("")
        assert empty_text == ""
        
        # Test URL normalization with edge cases
        weird_urls = ["", None, "#", "javascript:void(0)"]
        base_url = "https://example.com"
        
        for url in weird_urls:
            if url is not None:
                result = self.parser.normalize_url(url, base_url)
                # Should not raise exceptions
                assert isinstance(result, str)
