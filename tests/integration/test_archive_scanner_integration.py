"""
Integration tests for ArchiveScanner.
Tests interaction with ArchiveScraper and database repository.
"""

import pytest
from unittest.mock import patch, AsyncMock, Mock
from src.archive_scanner import ArchiveScanner
from src.dao.models import Review


class TestArchiveScannerIntegration:
    """Integration tests for ArchiveScanner with real components"""

    @pytest.fixture
    def archive_url(self):
        """Standard archive URL"""
        return "https://platypus1917.org/platypus-review/"

    @pytest.fixture
    def mock_archive_urls(self):
        """Mock URLs from archive"""
        return {
            "https://platypus1917.org/category/pr/issue-179/",
            "https://platypus1917.org/category/pr/issue-178/",
            "https://platypus1917.org/category/pr/issue-177/",
            "https://platypus1917.org/category/pr/issue-176/"
        }

    @pytest.fixture
    def mock_db_reviews(self):
        """Mock Review objects from database"""
        reviews = []
        for issue_num in [177, 176]:
            review = Mock(spec=Review)
            review.id = issue_num
            review.source_url = f"https://platypus1917.org/category/pr/issue-{issue_num}/"
            reviews.append(review)
        return reviews

    @pytest.mark.asyncio
    async def test_scan_workflow_integration(self, archive_url, mock_archive_urls):
        """Integration test: complete scan workflow"""
        # Create scanner
        scanner = ArchiveScanner(archive_url)
        
        # Mock both scraper and repository
        scanner.archive_scraper.get_listing_urls = Mock(return_value=mock_archive_urls)
        
        db_urls = {
            "https://platypus1917.org/category/pr/issue-177/",
            "https://platypus1917.org/category/pr/issue-176/"
        }
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(return_value=db_urls)
            
            # Execute scan
            result = await scanner.scan_for_new_reviews()
            
            # Verify workflow
            scanner.archive_scraper.get_listing_urls.assert_called_once()
            mock_repo.get_all_source_urls.assert_called_once()
            
            # Verify results
            assert 'new_reviews' in result
            assert 'existing_reviews' in result
            assert 'total_count' in result
            
            # Check categorization
            expected_new = {
                "https://platypus1917.org/category/pr/issue-179/",
                "https://platypus1917.org/category/pr/issue-178/"
            }
            assert result['new_reviews'] == expected_new
            assert result['existing_reviews'] == db_urls
            assert result['total_count'] == 4

    @pytest.mark.asyncio
    async def test_get_new_reviews_integration(self, archive_url, mock_archive_urls):
        """Integration test: get_new_reviews extracts only new URLs"""
        scanner = ArchiveScanner(archive_url)
        scanner.archive_scraper.get_listing_urls = Mock(return_value=mock_archive_urls)
        
        # Mock database with some existing reviews
        db_urls = {
            "https://platypus1917.org/category/pr/issue-177/",
            "https://platypus1917.org/category/pr/issue-176/"
        }
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(return_value=db_urls)
            
            new_reviews = await scanner.get_new_reviews()
            
            # Should return only the 2 new ones
            assert len(new_reviews) == 2
            assert "https://platypus1917.org/category/pr/issue-179/" in new_reviews
            assert "https://platypus1917.org/category/pr/issue-178/" in new_reviews

    @pytest.mark.asyncio
    async def test_check_reviews_in_db_integration(self, archive_url, mock_archive_urls):
        """Integration test: database check with bulk query"""
        scanner = ArchiveScanner(archive_url)
        
        # Mock database response
        db_urls = {
            "https://platypus1917.org/category/pr/issue-177/",
            "https://platypus1917.org/category/pr/issue-176/",
            "https://platypus1917.org/category/pr/issue-175/"  # Extra in DB
        }
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(return_value=db_urls)
            
            result = await scanner._check_reviews_in_db(mock_archive_urls)
            
            # Should return intersection
            expected_intersection = {
                "https://platypus1917.org/category/pr/issue-177/",
                "https://platypus1917.org/category/pr/issue-176/"
            }
            assert result == expected_intersection
            
            # Verify efficient bulk query was used (not N queries)
            assert mock_repo.get_all_source_urls.call_count == 1

    @pytest.mark.asyncio
    async def test_get_review_by_criteria_integration(self, archive_url):
        """Integration test: find review by ID from database"""
        scanner = ArchiveScanner(archive_url)
        
        # Mock review from database
        mock_review = Mock(spec=Review)
        mock_review.id = 179
        mock_review.source_url = "https://platypus1917.org/category/pr/issue-179/"
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_by_id = AsyncMock(return_value=mock_review)
            
            result = await scanner.get_review_by_criteria(review_id=179)
            
            mock_repo.get_by_id.assert_called_once_with(179)
            assert result == mock_review.source_url

    @pytest.mark.asyncio
    async def test_full_workflow_with_empty_database(self, archive_url, mock_archive_urls):
        """Integration test: scan with empty database (all reviews are new)"""
        scanner = ArchiveScanner(archive_url)
        scanner.archive_scraper.get_listing_urls = Mock(return_value=mock_archive_urls)
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(return_value=set())
            
            result = await scanner.scan_for_new_reviews()
            
            # All should be new
            assert result['new_reviews'] == mock_archive_urls
            assert result['existing_reviews'] == set()
            assert result['total_count'] == len(mock_archive_urls)

    @pytest.mark.asyncio
    async def test_full_workflow_with_all_existing(self, archive_url, mock_archive_urls):
        """Integration test: scan when all reviews already in database"""
        scanner = ArchiveScanner(archive_url)
        scanner.archive_scraper.get_listing_urls = Mock(return_value=mock_archive_urls)
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            # All reviews already in DB
            mock_repo.get_all_source_urls = AsyncMock(return_value=mock_archive_urls)
            
            result = await scanner.scan_for_new_reviews()
            
            # None should be new
            assert result['new_reviews'] == set()
            assert result['existing_reviews'] == mock_archive_urls
            assert result['total_count'] == len(mock_archive_urls)

    @pytest.mark.asyncio
    async def test_scraper_error_propagation(self, archive_url):
        """Integration test: errors from scraper propagate correctly"""
        scanner = ArchiveScanner(archive_url)
        scanner.archive_scraper.get_listing_urls = Mock(
            side_effect=Exception("Scraping failed")
        )
        
        with pytest.raises(Exception, match="Scraping failed"):
            await scanner.scan_for_new_reviews()

    @pytest.mark.asyncio
    async def test_database_error_propagation(self, archive_url, mock_archive_urls):
        """Integration test: database errors propagate correctly"""
        scanner = ArchiveScanner(archive_url)
        scanner.archive_scraper.get_listing_urls = Mock(return_value=mock_archive_urls)
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(
                side_effect=Exception("Database connection failed")
            )
            
            with pytest.raises(Exception, match="Database connection failed"):
                await scanner.scan_for_new_reviews()

    @pytest.mark.asyncio
    async def test_performance_with_large_dataset(self, archive_url):
        """Integration test: handle large number of URLs efficiently"""
        # Generate 200 archive URLs
        large_archive_urls = {
            f"https://platypus1917.org/category/pr/issue-{i}/"
            for i in range(1, 201)
        }
        
        # 150 already in database
        db_urls = {
            f"https://platypus1917.org/category/pr/issue-{i}/"
            for i in range(1, 151)
        }
        
        scanner = ArchiveScanner(archive_url)
        scanner.archive_scraper.get_listing_urls = Mock(return_value=large_archive_urls)
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(return_value=db_urls)
            
            import time
            start_time = time.time()
            
            result = await scanner.scan_for_new_reviews()
            
            elapsed = time.time() - start_time
            
            # Verify correctness
            assert len(result['new_reviews']) == 50
            assert len(result['existing_reviews']) == 150
            
            # Verify efficiency (should be very fast with bulk query)
            assert elapsed < 1.0, "Should complete in under 1 second with bulk query"
            
            # Verify only 1 database query (not 200!)
            assert mock_repo.get_all_source_urls.call_count == 1

    @pytest.mark.asyncio
    async def test_integration_with_realistic_scenario(self, archive_url):
        """Integration test: realistic scenario with mixed new/existing reviews"""
        # Archive has issues 175-180
        archive_urls = {
            f"https://platypus1917.org/category/pr/issue-{i}/"
            for i in range(175, 181)
        }
        
        # Database has issues 175-177 (older ones already processed)
        db_urls = {
            f"https://platypus1917.org/category/pr/issue-{i}/"
            for i in range(175, 178)
        }
        
        scanner = ArchiveScanner(archive_url)
        scanner.archive_scraper.get_listing_urls = Mock(return_value=archive_urls)
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(return_value=db_urls)
            
            result = await scanner.scan_for_new_reviews()
            
            # New reviews: 178, 179, 180
            expected_new = {
                "https://platypus1917.org/category/pr/issue-178/",
                "https://platypus1917.org/category/pr/issue-179/",
                "https://platypus1917.org/category/pr/issue-180/"
            }
            
            # Existing reviews: 175, 176, 177
            expected_existing = {
                "https://platypus1917.org/category/pr/issue-175/",
                "https://platypus1917.org/category/pr/issue-176/",
                "https://platypus1917.org/category/pr/issue-177/"
            }
            
            assert result['new_reviews'] == expected_new
            assert result['existing_reviews'] == expected_existing
            assert result['total_count'] == 6

    @pytest.mark.asyncio
    async def test_get_new_reviews_convenience_method(self, archive_url):
        """Integration test: get_new_reviews as convenience wrapper"""
        archive_urls = {
            "https://platypus1917.org/category/pr/issue-179/",
            "https://platypus1917.org/category/pr/issue-178/"
        }
        
        scanner = ArchiveScanner(archive_url)
        scanner.archive_scraper.get_listing_urls = Mock(return_value=archive_urls)
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(return_value=set())
            
            # Use convenience method
            new_reviews = await scanner.get_new_reviews()
            
            # Should be same as scan_for_new_reviews()['new_reviews']
            assert new_reviews == archive_urls
            assert isinstance(new_reviews, set)
