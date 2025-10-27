"""
Unit tests for ArchiveScanner.
Tests business logic for scanning archive and checking against database.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from src.archive_scanner import ArchiveScanner


@pytest.fixture
def archive_url():
    """Standard archive URL for testing"""
    return "https://platypus1917.org/platypus-review/"


@pytest.fixture
def archive_scanner(archive_url):
    """Create ArchiveScanner instance for testing"""
    with patch('src.archive_scanner.ArchiveScraper'):
        scanner = ArchiveScanner(archive_url)
        return scanner


@pytest.fixture
def mock_review_urls():
    """Mock set of review URLs from archive"""
    return {
        "https://platypus1917.org/category/pr/issue-179/",
        "https://platypus1917.org/category/pr/issue-178/",
        "https://platypus1917.org/category/pr/issue-177/",
        "https://platypus1917.org/category/pr/issue-176/"
    }


@pytest.fixture
def mock_db_urls():
    """Mock set of review URLs from database"""
    return {
        "https://platypus1917.org/category/pr/issue-177/",
        "https://platypus1917.org/category/pr/issue-176/"
    }


class TestArchiveScanner:
    """Test ArchiveScanner class"""
    
    def test_init_with_url(self, archive_url):
        """Test ArchiveScanner initialization with URL"""
        with patch('src.archive_scanner.ArchiveScraper') as mock_scraper_class:
            scanner = ArchiveScanner(archive_url)
            
            assert scanner.archive_url == archive_url
            mock_scraper_class.assert_called_once_with(archive_url)
    
    def test_init_with_env_url(self):
        """Test ArchiveScanner initialization with URL from environment"""
        env_url = "https://test.com/archive/"
        
        with patch('src.archive_scanner.ArchiveScraper') as mock_scraper_class, \
             patch.dict('os.environ', {'ARCHIVE_URL': env_url}):
            
            scanner = ArchiveScanner()
            
            assert scanner.archive_url == env_url
            mock_scraper_class.assert_called_once_with(env_url)
    
    def test_init_creates_archive_scraper(self, archive_scanner):
        """Test that init creates ArchiveScraper instance"""
        assert hasattr(archive_scanner, 'archive_scraper')
    
    @pytest.mark.asyncio
    async def test_get_new_reviews_success(self, archive_scanner):
        """Test get_new_reviews returns only new URLs"""
        new_urls = {
            "https://platypus1917.org/category/pr/issue-179/",
            "https://platypus1917.org/category/pr/issue-178/"
        }
        
        mock_result = {
            'new_reviews': new_urls,
            'existing_reviews': set(),
            'total_count': 2
        }
        
        with patch.object(archive_scanner, 'scan_for_new_reviews', new_callable=AsyncMock) as mock_scan:
            mock_scan.return_value = mock_result
            
            result = await archive_scanner.get_new_reviews()
            
            mock_scan.assert_called_once()
            assert result == new_urls
            assert isinstance(result, set)
    
    @pytest.mark.asyncio
    async def test_get_new_reviews_empty(self, archive_scanner):
        """Test get_new_reviews when no new reviews found"""
        mock_result = {
            'new_reviews': set(),
            'existing_reviews': {"url1", "url2"},
            'total_count': 2
        }
        
        with patch.object(archive_scanner, 'scan_for_new_reviews', new_callable=AsyncMock) as mock_scan:
            mock_scan.return_value = mock_result
            
            result = await archive_scanner.get_new_reviews()
            
            assert result == set()
            assert len(result) == 0
    
    @pytest.mark.asyncio
    async def test_scan_for_new_reviews_success(self, archive_scanner, mock_review_urls, mock_db_urls):
        """Test scan_for_new_reviews identifies new vs existing reviews"""
        archive_scanner.archive_scraper.get_listing_urls = Mock(return_value=mock_review_urls)
        
        with patch.object(archive_scanner, '_check_reviews_in_db', new_callable=AsyncMock) as mock_check:
            mock_check.return_value = mock_db_urls
            
            result = await archive_scanner.scan_for_new_reviews()
            
            # Verify scraper was called
            archive_scanner.archive_scraper.get_listing_urls.assert_called_once()
            
            # Verify database check was called with archive URLs
            mock_check.assert_called_once_with(mock_review_urls)
            
            # Verify correct categorization
            assert 'new_reviews' in result
            assert 'existing_reviews' in result
            assert 'total_count' in result
            
            expected_new = mock_review_urls - mock_db_urls
            expected_existing = mock_review_urls & mock_db_urls
            
            assert result['new_reviews'] == expected_new
            assert result['existing_reviews'] == expected_existing
            assert result['total_count'] == len(mock_review_urls)
    
    @pytest.mark.asyncio
    async def test_scan_for_new_reviews_all_new(self, archive_scanner, mock_review_urls):
        """Test scan_for_new_reviews when all reviews are new"""
        archive_scanner.archive_scraper.get_listing_urls = Mock(return_value=mock_review_urls)
        
        with patch.object(archive_scanner, '_check_reviews_in_db', new_callable=AsyncMock) as mock_check:
            mock_check.return_value = set()  # No reviews in DB
            
            result = await archive_scanner.scan_for_new_reviews()
            
            assert result['new_reviews'] == mock_review_urls
            assert result['existing_reviews'] == set()
            assert len(result['new_reviews']) == 4
    
    @pytest.mark.asyncio
    async def test_scan_for_new_reviews_all_existing(self, archive_scanner, mock_review_urls):
        """Test scan_for_new_reviews when all reviews exist in DB"""
        archive_scanner.archive_scraper.get_listing_urls = Mock(return_value=mock_review_urls)
        
        with patch.object(archive_scanner, '_check_reviews_in_db', new_callable=AsyncMock) as mock_check:
            mock_check.return_value = mock_review_urls  # All in DB
            
            result = await archive_scanner.scan_for_new_reviews()
            
            assert result['new_reviews'] == set()
            assert result['existing_reviews'] == mock_review_urls
            assert len(result['existing_reviews']) == 4
    
    @pytest.mark.asyncio
    async def test_scan_for_new_reviews_empty_archive(self, archive_scanner):
        """Test scan_for_new_reviews with empty archive"""
        archive_scanner.archive_scraper.get_listing_urls = Mock(return_value=set())
        
        with patch.object(archive_scanner, '_check_reviews_in_db', new_callable=AsyncMock) as mock_check:
            mock_check.return_value = set()
            
            result = await archive_scanner.scan_for_new_reviews()
            
            assert result['new_reviews'] == set()
            assert result['existing_reviews'] == set()
            assert result['total_count'] == 0
    
    @pytest.mark.asyncio
    async def test_check_reviews_in_db_bulk_query(self, archive_scanner, mock_review_urls, mock_db_urls):
        """Test _check_reviews_in_db uses bulk query approach"""
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(return_value=mock_db_urls)
            
            result = await archive_scanner._check_reviews_in_db(mock_review_urls)
            
            # Verify bulk query was called once
            mock_repo.get_all_source_urls.assert_called_once()
            
            # Verify correct intersection
            expected = mock_review_urls & mock_db_urls
            assert result == expected
    
    @pytest.mark.asyncio
    async def test_check_reviews_in_db_no_matches(self, archive_scanner, mock_review_urls):
        """Test _check_reviews_in_db when no reviews exist in DB"""
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(return_value=set())
            
            result = await archive_scanner._check_reviews_in_db(mock_review_urls)
            
            assert result == set()
    
    @pytest.mark.asyncio
    async def test_check_reviews_in_db_all_match(self, archive_scanner, mock_review_urls):
        """Test _check_reviews_in_db when all reviews exist in DB"""
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_all_source_urls = AsyncMock(return_value=mock_review_urls)
            
            result = await archive_scanner._check_reviews_in_db(mock_review_urls)
            
            assert result == mock_review_urls
    
    @pytest.mark.asyncio
    async def test_get_review_by_criteria_by_id_found_in_db(self, archive_scanner):
        """Test get_review_by_criteria finds review by ID in database"""
        review_id = 179
        expected_url = "https://platypus1917.org/category/pr/issue-179/"
        
        mock_review = Mock()
        mock_review.id = review_id
        mock_review.source_url = expected_url
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_by_id = AsyncMock(return_value=mock_review)
            
            result = await archive_scanner.get_review_by_criteria(review_id=review_id)
            
            mock_repo.get_by_id.assert_called_once_with(review_id)
            assert result == expected_url
    
    @pytest.mark.asyncio
    async def test_get_review_by_criteria_by_id_not_found(self, archive_scanner):
        """Test get_review_by_criteria when review not in database"""
        review_id = 999
        
        with patch('src.archive_scanner.review_repository') as mock_repo:
            mock_repo.get_by_id = AsyncMock(return_value=None)
            
            result = await archive_scanner.get_review_by_criteria(review_id=review_id)
            
            # Currently returns None when not in DB (archive search not implemented)
            assert result is None
    
    @pytest.mark.asyncio
    async def test_get_review_by_criteria_no_criteria(self, archive_scanner):
        """Test get_review_by_criteria with no criteria provided"""
        result = await archive_scanner.get_review_by_criteria()
        
        # Should return None when no criteria provided
        assert result is None
    
    @pytest.mark.asyncio
    async def test_logging_occurs(self, archive_scanner, caplog):
        """Test that appropriate logging occurs during operations"""
        import logging
        
        with caplog.at_level(logging.INFO):
            archive_scanner.archive_scraper.get_listing_urls = Mock(return_value={"url1", "url2"})
            
            with patch.object(archive_scanner, '_check_reviews_in_db', new_callable=AsyncMock) as mock_check:
                mock_check.return_value = {"url1"}
                
                await archive_scanner.scan_for_new_reviews()
                
                # Check for expected log messages
                assert "Starting archive scan" in caplog.text
                assert "Found 2 review URLs in archive" in caplog.text
                assert "Found 1 existing reviews in database" in caplog.text
                assert "Scan complete: 1 new, 1 existing" in caplog.text
