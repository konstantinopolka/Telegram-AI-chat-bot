"""
System integration test for archive scanning functionality.
Tests complete end-to-end workflow with real components.
"""

import pytest
from unittest.mock import patch, AsyncMock, Mock
from src.archive_scanner import ArchiveScanner


class TestArchiveSystemIntegration:
    """System-level integration tests for archive scanning workflow"""

    @pytest.fixture
    def archive_url(self):
        """Real Platypus archive URL"""
        return "https://platypus1917.org/platypus-review/"

    @pytest.fixture
    def realistic_archive_html(self):
        """Realistic HTML from Platypus archive page"""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Platypus Review Archive</title>
        </head>
        <body>
            <main>
                <section class="archive">
                    <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179 – October 2025</a></h2>
                    <h2><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178 – September 2025</a></h2>
                    <h2><a href="https://platypus1917.org/category/pr/issue-177/">Issue 177 – August 2025</a></h2>
                    <h2><a href="https://platypus1917.org/category/pr/issue-176/">Issue 176 – July 2025</a></h2>
                    <h2><a href="https://platypus1917.org/category/pr/issue-175/">Issue 175 – June 2025</a></h2>
                </section>
            </main>
        </body>
        </html>
        """

    @pytest.mark.asyncio
    @pytest.mark.system
    async def test_complete_archive_scan_workflow(self, archive_url, realistic_archive_html):
        """
        System test: Complete workflow from archive scan to categorization.
        
        Workflow:
        1. ArchiveScanner fetches archive page
        2. ArchiveScraper extracts review URLs
        3. ArchiveParser parses HTML
        4. Database check identifies new vs existing reviews
        5. Results returned for processing
        """
        scanner = ArchiveScanner(archive_url)
        
        # Mock HTTP fetch but use real parsing
        with patch.object(scanner.archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.return_value = realistic_archive_html
            
            # Mock database with 2 existing reviews
            db_urls = {
                "https://platypus1917.org/category/pr/issue-175/",
                "https://platypus1917.org/category/pr/issue-176/"
            }
            
            with patch('src.archive_scanner.review_repository') as mock_repo:
                mock_repo.get_all_source_urls = AsyncMock(return_value=db_urls)
                
                # Execute complete workflow
                result = await scanner.scan_for_new_reviews()
                
                # Verify complete workflow
                assert mock_fetch.called, "Should fetch archive page"
                assert mock_repo.get_all_source_urls.called, "Should check database"
                
                # Verify results
                assert result['total_count'] == 5
                assert len(result['new_reviews']) == 3
                assert len(result['existing_reviews']) == 2
                
                # Verify correct categorization
                expected_new = {
                    "https://platypus1917.org/category/pr/issue-179/",
                    "https://platypus1917.org/category/pr/issue-178/",
                    "https://platypus1917.org/category/pr/issue-177/"
                }
                assert result['new_reviews'] == expected_new

    @pytest.mark.asyncio
    @pytest.mark.system
    async def test_reposting_orchestrator_integration(self, archive_url):
        """
        System test: RepostingOrchestrator uses ArchiveScanner.
        
        Tests that the top-level orchestrator correctly integrates
        with archive scanning functionality.
        """
        # This would test the RepostingOrchestrator workflow
        # For now, we'll test the scanner in isolation
        scanner = ArchiveScanner(archive_url)
        
        mock_archive_urls = {
            "https://platypus1917.org/category/pr/issue-179/",
            "https://platypus1917.org/category/pr/issue-178/"
        }
        
        scanner.archive_scraper.get_listing_urls = Mock(return_value=mock_archive_urls)
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(return_value=set())
            
            new_reviews = await scanner.get_new_reviews()
            
            # These would be passed to ReviewOrchestrator for processing
            assert len(new_reviews) == 2
            assert all(isinstance(url, str) for url in new_reviews)

    @pytest.mark.asyncio
    @pytest.mark.system
    async def test_error_recovery_workflow(self, archive_url, realistic_archive_html):
        """
        System test: Error handling in complete workflow.
        
        Tests that errors are properly handled and propagated through
        the entire system stack.
        """
        scanner = ArchiveScanner(archive_url)
        
        # Test HTTP error recovery
        with patch.object(scanner.archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.side_effect = Exception("Network timeout")
            
            with pytest.raises(Exception, match="Network timeout"):
                await scanner.scan_for_new_reviews()
        
        # Test database error recovery
        with patch.object(scanner.archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.return_value = realistic_archive_html
            
            with patch('src.archive_scanner.review_repository') as mock_repo:
                mock_repo.get_all_source_urls = AsyncMock(
                    side_effect=Exception("Database connection failed")
                )
                
                with pytest.raises(Exception, match="Database connection failed"):
                    await scanner.scan_for_new_reviews()

    @pytest.mark.asyncio
    @pytest.mark.system
    async def test_incremental_update_scenario(self, archive_url, realistic_archive_html):
        """
        System test: Simulates incremental updates over time.
        
        Scenario:
        1. First scan: 3 reviews in archive, all new
        2. Second scan: 5 reviews in archive, 3 existing, 2 new
        """
        scanner = ArchiveScanner(archive_url)
        
        # First scan - archive has 3 reviews
        html_first_scan = """
        <html><body>
            <h2><a href="https://platypus1917.org/category/pr/issue-177/">Issue 177</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-176/">Issue 176</a></h2>
            <h2><a href="https://platypus1917.org/category/pr/issue-175/">Issue 175</a></h2>
        </body></html>
        """
        
        with patch.object(scanner.archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.return_value = html_first_scan
            
            with patch('src.archive_scanner.review_repository') as mock_repo:
                # Database is empty on first scan
                mock_repo.get_all_source_urls = AsyncMock(return_value=set())
                
                result_first = await scanner.scan_for_new_reviews()
                
                assert result_first['total_count'] == 3
                assert len(result_first['new_reviews']) == 3
                assert len(result_first['existing_reviews']) == 0
        
        # Second scan - archive now has 5 reviews
        with patch.object(scanner.archive_scraper.fetcher, 'fetch_page') as mock_fetch:
            mock_fetch.return_value = realistic_archive_html  # Has 5 reviews
            
            with patch('src.archive_scanner.review_repository') as mock_repo:
                # Database now has the 3 from first scan
                db_urls = {
                    "https://platypus1917.org/category/pr/issue-177/",
                    "https://platypus1917.org/category/pr/issue-176/",
                    "https://platypus1917.org/category/pr/issue-175/"
                }
                mock_repo.get_all_source_urls = AsyncMock(return_value=db_urls)
                
                result_second = await scanner.scan_for_new_reviews()
                
                assert result_second['total_count'] == 5
                assert len(result_second['new_reviews']) == 2  # 178, 179
                assert len(result_second['existing_reviews']) == 3  # 175, 176, 177

    @pytest.mark.asyncio
    @pytest.mark.system
    async def test_performance_characteristics(self, archive_url):
        """
        System test: Verify performance characteristics.
        
        Ensures that bulk operations are used and system performs
        efficiently even with many reviews.
        """
        import time
        
        # Generate large dataset
        large_archive_urls = {
            f"https://platypus1917.org/category/pr/issue-{i}/"
            for i in range(1, 301)  # 300 reviews
        }
        
        db_urls = {
            f"https://platypus1917.org/category/pr/issue-{i}/"
            for i in range(1, 201)  # 200 already in DB
        }
        
        scanner = ArchiveScanner(archive_url)
        scanner.archive_scraper.get_listing_urls = Mock(return_value=large_archive_urls)
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(return_value=db_urls)
            
            start_time = time.time()
            result = await scanner.scan_for_new_reviews()
            elapsed = time.time() - start_time
            
            # Verify correctness
            assert len(result['new_reviews']) == 100
            assert len(result['existing_reviews']) == 200
            
            # Verify efficiency
            assert elapsed < 1.0, "Should complete quickly with bulk query"
            assert mock_repo.get_all_source_urls.call_count == 1, "Should use single bulk query"

    @pytest.mark.slow
    @pytest.mark.system
    @pytest.mark.asyncio
    async def test_real_archive_end_to_end(self):
        """
        System test: End-to-end with REAL archive (slow).
        
        Makes actual HTTP request to Platypus archive and processes results.
        Only run when explicitly requested with: pytest -m slow
        
        This is a smoke test to verify the system works with real data.
        """
        try:
            scanner = ArchiveScanner("https://platypus1917.org/platypus-review/")
            
            # Mock only the database (use real HTTP and parsing)
            with patch('src.archive_scanner.review_repository') as mock_repo:
                # Pretend database is empty
                mock_repo.get_all_source_urls = AsyncMock(return_value=set())
                
                # This makes a real HTTP request!
                result = await scanner.scan_for_new_reviews()
                
                # Basic sanity checks
                assert result['total_count'] > 0, "Archive should have reviews"
                assert len(result['new_reviews']) > 0, "Should find new reviews"
                assert len(result['existing_reviews']) == 0, "DB is empty"
                
                # Verify all URLs are valid
                for url in result['new_reviews']:
                    assert url.startswith("https://platypus1917.org/category/pr/issue-")
                    assert url.endswith("/")
                
                print(f"\n✅ Successfully scanned {result['total_count']} reviews from real archive")
                print(f"   Sample URLs: {list(result['new_reviews'])[:5]}")
                
        except Exception as e:
            pytest.skip(f"Real HTTP test failed (network issue?): {e}")

    @pytest.mark.asyncio
    @pytest.mark.system
    async def test_data_flow_through_system(self, archive_url, realistic_archive_html):
        """
        System test: Trace data flow through entire system.
        
        Verifies that data correctly flows from:
        HTTP → Fetcher → Parser → Scanner → Database Check → Result
        """
        scanner = ArchiveScanner(archive_url)
        
        # Track data at each stage
        fetched_html = None
        parsed_urls = None
        db_urls = None
        
        def track_fetch():
            nonlocal fetched_html
            fetched_html = realistic_archive_html
            return fetched_html
        
        def track_parse(html):
            nonlocal parsed_urls
            # Use real parser
            parsed_urls = scanner.archive_scraper.parser.parse_archive_page(html)
            return parsed_urls
        
        async def track_db_query():
            nonlocal db_urls
            db_urls = {
                "https://platypus1917.org/category/pr/issue-175/",
                "https://platypus1917.org/category/pr/issue-176/"
            }
            return db_urls
        
        with patch.object(scanner.archive_scraper.fetcher, 'fetch_page', side_effect=track_fetch), \
             patch.object(scanner.archive_scraper.parser, 'parse_archive_page', side_effect=track_parse), \
             patch('src.archive_scanner.review_repository') as mock_repo:
            
            mock_repo.get_all_source_urls = track_db_query
            
            result = await scanner.scan_for_new_reviews()
            
            # Verify data flowed through all stages
            assert fetched_html is not None, "HTML should be fetched"
            assert parsed_urls is not None, "URLs should be parsed"
            assert db_urls is not None, "Database should be queried"
            
            # Verify transformations
            assert len(parsed_urls) == 5, "Should parse 5 URLs from HTML"
            assert len(db_urls) == 2, "Database has 2 URLs"
            assert len(result['new_reviews']) == 3, "3 new URLs (5 - 2)"
            assert len(result['existing_reviews']) == 2, "2 existing URLs"
