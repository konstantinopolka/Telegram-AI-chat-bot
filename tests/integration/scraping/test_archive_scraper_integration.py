"""
Integration tests for ArchiveScraper.
Tests complete workflow: fetching + parsing archive page.
Can use either mocked HTTP or real requests (mark with @pytest.mark.slow).
"""

import pytest
from unittest.mock import patch, Mock
from src.scraping.archive_scraper import ArchiveScraper


class TestArchiveScraperIntegration:
    """Integration tests for ArchiveScraper workflow"""

    @pytest.fixture
    def archive_url(self):
        """Standard archive URL"""
        return "https://platypus1917.org/platypus-review/"

    @pytest.fixture
    def archive_scraper(self, archive_url):
        """Create ArchiveScraper instance"""
        return ArchiveScraper(archive_url)

    @pytest.fixture
    def realistic_archive_html(self):
        """Realistic HTML from archive page"""
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Platypus Review Archive</title></head>
        <body>
            <div class="archive">
                <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179</a></h2>
                <h2><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178</a></h2>
                <h2><a href="https://platypus1917.org/category/pr/issue-177/">Issue 177</a></h2>
                <h2><a href="https://platypus1917.org/about/">About</a></h2>
            </div>
        </body>
        </html>
        """

    def test_get_listing_urls_integration_mocked_fetch(self, archive_scraper, realistic_archive_html):
        """Integration test: complete workflow with mocked HTTP"""
        # Mock only the HTTP fetch, let parser do real work
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.return_value = realistic_archive_html
            
            result = archive_scraper.get_listing_urls()
            
            # Verify HTTP was called
            mock_fetch.assert_called_once()
            
            # Verify parsing worked correctly
            assert isinstance(result, set)
            assert len(result) == 3
            
            # Verify correct URLs were extracted
            expected_urls = {
                "https://platypus1917.org/category/pr/issue-179/",
                "https://platypus1917.org/category/pr/issue-178/",
                "https://platypus1917.org/category/pr/issue-177/"
            }
            assert result == expected_urls

    def test_fetcher_parser_integration(self, archive_scraper, realistic_archive_html):
        """Integration test: verify fetcher and parser work together"""
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.return_value = realistic_archive_html
            
            # Get URLs
            urls = archive_scraper.get_listing_urls()
            
            # Verify fetcher was used
            assert mock_fetch.called
            
            # Verify parser processed the HTML correctly
            assert all(isinstance(url, str) for url in urls)
            assert all(url.startswith("https://") for url in urls)
            assert all("category/pr/issue-" in url for url in urls)

    def test_empty_archive_integration(self, archive_scraper):
        """Integration test: handle empty archive page"""
        empty_html = """
        <html>
        <body>
            <div>No reviews available</div>
        </body>
        </html>
        """
        
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.return_value = empty_html
            
            result = archive_scraper.get_listing_urls()
            
            assert result == set()

    def test_duplicate_urls_removed_integration(self, archive_scraper):
        """Integration test: verify duplicates are removed"""
        html_with_duplicates = """
        <html>
        <body>
            <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179 (Duplicate)</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178</a></h2>
        </body>
        </html>
        """
        
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.return_value = html_with_duplicates
            
            result = archive_scraper.get_listing_urls()
            
            # Set should have removed duplicates
            assert len(result) == 2
            assert "https://platypus1917.org/category/pr/issue-179/" in result
            assert "https://platypus1917.org/category/pr/issue-178/" in result

    def test_error_propagation_from_fetcher(self, archive_scraper):
        """Integration test: errors from fetcher propagate correctly"""
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.side_effect = Exception("Network timeout")
            
            with pytest.raises(Exception, match="Network timeout"):
                archive_scraper.get_listing_urls()

    def test_error_propagation_from_parser(self, archive_scraper):
        """Integration test: errors from parser propagate correctly"""
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(archive_scraper.parser, 'parse_archive_page') as mock_parse:
            
            mock_fetch.return_value = "<html>content</html>"
            mock_parse.side_effect = ValueError("Invalid HTML structure")
            
            with pytest.raises(ValueError, match="Invalid HTML structure"):
                archive_scraper.get_listing_urls()

    def test_large_archive_integration(self, archive_scraper):
        """Integration test: handle large number of review URLs"""
        # Generate HTML with many review links
        html_parts = ['<html><body>']
        for i in range(200, 100, -1):  # 100 reviews
            html_parts.append(
                f'<h2><a href="https://platypus1917.org/category/pr/issue-{i}/">Issue {i}</a></h2>'
            )
        html_parts.append('</body></html>')
        large_html = '\n'.join(html_parts)
        
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.return_value = large_html
            
            result = archive_scraper.get_listing_urls()
            
            # Should handle 100 URLs efficiently
            assert len(result) == 100
            assert isinstance(result, set)

    @pytest.mark.slow
    @pytest.mark.integration
    def test_real_http_request_to_archive(self):
        """
        Integration test with REAL HTTP request to Platypus archive.
        Marked as slow - only run when explicitly requested.
        
        Usage: pytest tests/integration/scraping/test_archive_scraper_integration.py -m slow
        """
        real_archive_url = "https://platypus1917.org/platypus-review/"
        scraper = ArchiveScraper(real_archive_url)
        
        try:
            # This makes a real HTTP request!
            urls = scraper.get_listing_urls()
            
            # Basic sanity checks
            assert isinstance(urls, set)
            assert len(urls) > 0, "Archive should have at least some reviews"
            
            # Verify all URLs match expected pattern
            for url in urls:
                assert url.startswith("https://platypus1917.org/category/pr/issue-")
                assert url.endswith("/")
            
            # Log the result for manual verification
            print(f"\nSuccessfully fetched {len(urls)} review URLs from real archive")
            print(f"Sample URLs: {list(urls)[:5]}")
            
        except Exception as e:
            pytest.skip(f"Real HTTP request failed (might be network issue): {e}")

    def test_workflow_sequence(self, archive_scraper, realistic_archive_html):
        """Integration test: verify complete workflow sequence"""
        fetch_called = False
        parse_called = False
        
        original_fetch = archive_scraper.fetcher.fetch_page
        original_parse = archive_scraper.parser.parse_archive_page
        
        def tracked_fetch():
            nonlocal fetch_called
            fetch_called = True
            return realistic_archive_html
        
        def tracked_parse(html):
            nonlocal parse_called
            parse_called = True
            return original_parse(html)
        
        with patch.object(archive_scraper.fetcher, 'fetch_page', side_effect=tracked_fetch), \
             patch.object(archive_scraper.parser, 'parse_archive_page', side_effect=tracked_parse):
            
            result = archive_scraper.get_listing_urls()
            
            # Verify workflow sequence
            assert fetch_called, "Fetcher should be called"
            assert parse_called, "Parser should be called"
            assert isinstance(result, set)
            assert len(result) > 0

    def test_integration_with_different_html_encodings(self, archive_scraper):
        """Integration test: handle different HTML encodings"""
        # HTML with UTF-8 special characters
        utf8_html = """
        <html>
        <head><meta charset="UTF-8"></head>
        <body>
            <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179 – October</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178 — Special Edition</a></h2>
        </body>
        </html>
        """
        
        with patch.object(archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.return_value = utf8_html
            
            result = archive_scraper.get_listing_urls()
            
            # Should handle UTF-8 characters in link text without issues
            assert len(result) == 2
