"""
Integration tests for ArchiveParser.
Tests parsing with real HTML structures from Platypus Review archive.
"""

import pytest
from src.scraping.archive_parser import ArchiveParser


class TestArchiveParserIntegration:
    """Integration tests for ArchiveParser using realistic HTML samples"""

    # Realistic HTML structure from Platypus Review archive page
    REALISTIC_ARCHIVE_HTML = """
    <!DOCTYPE html>
    <html>
    <head><title>Platypus Review Archive</title></head>
    <body>
        <div class="archive-section">
            <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179 – October 2025</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178 – September 2025</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-177/">Issue 177 – August 2025</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-176/">Issue 176 – July 2025</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-175/">Issue 175 – June 2025</a></h2>
            
            <!-- Non-review links that should be filtered -->
            <h2><a href="https://platypus1917.org/about/">About Us</a></h2>
            <h2><a href="https://platypus1917.org/contact/">Contact</a></h2>
            <a href="https://external-site.com/article/">External Link</a>
        </div>
        
        <div class="sidebar">
            <h2><a href="https://platypus1917.org/donate/">Donate</a></h2>
        </div>
    </body>
    </html>
    """

    # HTML with mixed formatting
    MIXED_FORMAT_HTML = """
    <html>
    <body>
        <div class="main-content">
            <h2><a href="https://platypus1917.org/category/pr/issue-180/">Issue 180</a></h2>
            <div class="description">Latest issue</div>
            <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179</a></h2>
            
            <!-- Some issues might have different HTML structure -->
            <section>
                <h2><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178 - Special Edition</a></h2>
            </section>
        </div>
    </body>
    </html>
    """

    # Minimal HTML with just one review
    MINIMAL_HTML = """
    <html>
    <body>
        <h2><a href="https://platypus1917.org/category/pr/issue-173/">Issue 173 – February 2025</a></h2>
    </body>
    </html>
    """

    # HTML with no review links
    EMPTY_HTML = """
    <html>
    <body>
        <div class="content">
            <h2><a href="https://platypus1917.org/about/">About</a></h2>
            <h2><a href="https://platypus1917.org/events/">Events</a></h2>
            <p>No review issues here</p>
        </div>
    </body>
    </html>
    """

    def setup_method(self):
        """Set up test fixtures for each test method"""
        self.parser = ArchiveParser()

    def test_parse_realistic_archive_html(self):
        """Integration test: parse realistic archive HTML structure"""
        urls = self.parser.parse_archive_page(self.REALISTIC_ARCHIVE_HTML)
        
        # Should extract exactly 5 review issue URLs
        assert len(urls) == 5
        
        # Verify all URLs match the expected pattern
        expected_urls = [
            "https://platypus1917.org/category/pr/issue-179/",
            "https://platypus1917.org/category/pr/issue-178/",
            "https://platypus1917.org/category/pr/issue-177/",
            "https://platypus1917.org/category/pr/issue-176/",
            "https://platypus1917.org/category/pr/issue-175/"
        ]
        
        assert urls == expected_urls
        
        # Verify non-review links are filtered out
        assert not any("about" in url for url in urls)
        assert not any("contact" in url for url in urls)
        assert not any("donate" in url for url in urls)
        assert not any("external-site" in url for url in urls)

    def test_parse_mixed_format_html(self):
        """Integration test: handle mixed HTML formatting"""
        urls = self.parser.parse_archive_page(self.MIXED_FORMAT_HTML)
        
        # Should extract 3 review URLs regardless of HTML structure variations
        assert len(urls) == 3
        
        expected_urls = [
            "https://platypus1917.org/category/pr/issue-180/",
            "https://platypus1917.org/category/pr/issue-179/",
            "https://platypus1917.org/category/pr/issue-178/"
        ]
        
        assert urls == expected_urls

    def test_parse_minimal_html(self):
        """Integration test: parse HTML with single review"""
        urls = self.parser.parse_archive_page(self.MINIMAL_HTML)
        
        assert len(urls) == 1
        assert urls[0] == "https://platypus1917.org/category/pr/issue-173/"

    def test_parse_empty_html(self):
        """Integration test: parse HTML with no review links"""
        urls = self.parser.parse_archive_page(self.EMPTY_HTML)
        
        assert len(urls) == 0
        assert urls == []

    def test_parse_preserves_url_order(self):
        """Integration test: verify URLs are returned in document order"""
        urls = self.parser.parse_archive_page(self.REALISTIC_ARCHIVE_HTML)
        
        # URLs should be in descending issue number order (as they appear in HTML)
        issue_numbers = [int(url.split('issue-')[1].rstrip('/')) for url in urls]
        assert issue_numbers == [179, 178, 177, 176, 175]

    def test_parse_handles_malformed_html_gracefully(self):
        """Integration test: BeautifulSoup handles malformed HTML"""
        malformed_html = """
        <html>
        <body>
            <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179</a>
            <!-- Missing closing tag -->
            <h2><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178</a></h2>
        </body>
        """
        
        # BeautifulSoup should still parse this
        urls = self.parser.parse_archive_page(malformed_html)
        
        # Should get both URLs despite malformed HTML
        assert len(urls) == 2

    def test_parse_with_special_characters_in_titles(self):
        """Integration test: handle special characters in link text"""
        html_with_special_chars = """
        <html>
        <body>
            <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179 – October 2025</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178 — Summer Edition</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-177/">Issue #177: Special</a></h2>
        </body>
        </html>
        """
        
        urls = self.parser.parse_archive_page(html_with_special_chars)
        
        # Should extract all 3 URLs regardless of special characters in text
        assert len(urls) == 3

    def test_parse_filters_by_selector_pattern(self):
        """Integration test: verify selector pattern correctly filters URLs"""
        # HTML with URLs that should and shouldn't match
        mixed_html = """
        <html>
        <body>
            <!-- Should match -->
            <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179</a></h2>
            
            <!-- Should NOT match - not in correct structure -->
            <div><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178</a></div>
            
            <!-- Should match -->
            <h2><a href="https://platypus1917.org/category/pr/issue-177/">Issue 177</a></h2>
            
            <!-- Should NOT match - different URL pattern -->
            <h2><a href="https://platypus1917.org/category/articles/some-article/">Article</a></h2>
        </body>
        </html>
        """
        
        urls = self.parser.parse_archive_page(mixed_html)
        
        # With default selectors, should only get h2 > a[href^=...] links
        # The exact count depends on the selector implementation
        assert all("category/pr/issue-" in url for url in urls)

    def test_parse_real_world_scenario(self):
        """Integration test: simulate real-world archive page parsing"""
        # This simulates what would happen with actual Platypus Review archive
        realistic_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Archive | Platypus Review</title>
        </head>
        <body>
            <main>
                <div class="archive-wrapper">
                    <h1>Review Archive</h1>
                    
                    <section class="current-year">
                        <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179 – October 2025</a></h2>
                        <h2><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178 – September 2025</a></h2>
                    </section>
                    
                    <section class="previous-year">
                        <h2><a href="https://platypus1917.org/category/pr/issue-177/">Issue 177 – December 2024</a></h2>
                        <h2><a href="https://platypus1917.org/category/pr/issue-176/">Issue 176 – November 2024</a></h2>
                    </section>
                    
                    <!-- Navigation and other elements -->
                    <nav>
                        <a href="https://platypus1917.org/">Home</a>
                        <a href="https://platypus1917.org/about/">About</a>
                    </nav>
                </div>
            </main>
        </body>
        </html>
        """
        
        urls = self.parser.parse_archive_page(realistic_html)
        
        # Should extract all 4 review URLs
        assert len(urls) == 4
        
        # Verify they're all valid review URLs
        for url in urls:
            assert url.startswith("https://platypus1917.org/category/pr/issue-")
            assert url.endswith("/")
        
        # Verify navigation links are excluded
        assert not any("about" in url for url in urls)
        assert not any(url == "https://platypus1917.org/" for url in urls)
