"""
Real-world integration test for ArchiveScanner.
Tests scanning the actual Platypus Review archive and identifying new reviews.

This test makes REAL HTTP requests to https://platypus1917.org/platypus-review/
and checks the database to categorize reviews as new or existing.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Set
import pytest

from src.archive_scanner import ArchiveScanner
from src.dao import review_repository
from src.logging_config import get_logger

logger = get_logger(__name__)

# Real archive URL (also set in .env)
ARCHIVE_URL = "https://platypus1917.org/platypus-review/"

class TestArchiveScannerReal:
    """Real-world integration tests for ArchiveScanner with live data"""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_archive_scanner_with_real_archive(self):
        """
        Test ArchiveScanner with real Platypus archive.
        
        Workflow:
        1. Create ArchiveScanner instance
        2. Scan real archive page (makes HTTP request)
        3. Get all review URLs from archive
        4. Check which reviews exist in database
        5. Categorize as new vs existing
        6. Verify results
        """
        logger.info("=" * 60)
        logger.info("Testing ArchiveScanner with Real Archive")
        logger.info("=" * 60)
        
        # Initialize scanner
        logger.info(f"Initializing ArchiveScanner for: {ARCHIVE_URL}")
        scanner = ArchiveScanner(ARCHIVE_URL)
        
        # Scan for new reviews (makes real HTTP request)
        logger.info("\n📡 Fetching review URLs from real archive...")
        result = await scanner.scan_for_new_reviews()
        
        # Verify result structure
        assert 'new_reviews' in result, "Result should contain 'new_reviews'"
        assert 'existing_reviews' in result, "Result should contain 'existing_reviews'"
        assert 'total_count' in result, "Result should contain 'total_count'"
        
        # Extract data
        new_reviews: Set[str] = result['new_reviews']
        existing_reviews: Set[str] = result['existing_reviews']
        total_count: int = result['total_count']
        
        # Log results
        logger.info("\n" + "=" * 60)
        logger.info("Archive Scan Results:")
        logger.info("=" * 60)
        logger.info(f"Total reviews in archive: {total_count}")
        logger.info(f"New reviews found: {len(new_reviews)}")
        logger.info(f"Existing reviews in DB: {len(existing_reviews)}")
        logger.info("=" * 60)
        
        # Verify we found reviews
        assert total_count > 0, "Archive should contain at least some reviews"
        assert len(new_reviews) + len(existing_reviews) == total_count, \
            "New + existing should equal total"
        
        # Verify all URLs are valid Platypus review URLs
        all_urls = new_reviews | existing_reviews
        for url in all_urls:
            assert url.startswith("https://platypus1917.org/category/pr/issue-"), \
                f"Invalid review URL format: {url}"
            assert url.endswith("/"), f"Review URL should end with /: {url}"
        
        # Log sample URLs
        if new_reviews:
            logger.info(f"\n📝 Sample new review URLs (showing up to 5):")
            for i, url in enumerate(list(new_reviews)[:5], 1):
                logger.info(f"  {i}. {url}")
        else:
            logger.info("\n✓ No new reviews found (all are already in database)")
        
        if existing_reviews:
            logger.info(f"\n💾 Sample existing review URLs (showing up to 3):")
            for i, url in enumerate(list(existing_reviews)[:3], 1):
                logger.info(f"  {i}. {url}")
        
        logger.info("\n✅ Archive scan completed successfully!")
        
        return result
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_new_reviews_convenience_method(self):
        """
        Test the get_new_reviews() convenience method with real archive.
        
        This is the method called by RepostingOrchestrator.
        """
        logger.info("=" * 60)
        logger.info("Testing get_new_reviews() with Real Archive")
        logger.info("=" * 60)
        
        # Initialize scanner
        scanner = ArchiveScanner(ARCHIVE_URL)
        
        # Get new reviews (this is what RepostingOrchestrator calls)
        logger.info("\n📡 Calling get_new_reviews() (as RepostingOrchestrator does)...")
        new_reviews: Set[str] = await scanner.get_new_reviews()
        
        # Verify result
        assert isinstance(new_reviews, set), "Should return a set of URLs"
        
        logger.info(f"\n✅ Found {len(new_reviews)} new review(s)")
        
        if new_reviews:
            logger.info("\n📋 New review URLs:")
            for i, url in enumerate(sorted(new_reviews), 1):
                # Extract issue number from URL
                issue_num = url.split('issue-')[1].rstrip('/')
                logger.info(f"  {i}. Issue {issue_num}: {url}")
        else:
            logger.info("\n✓ No new reviews (all reviews already in database)")
        
        # Verify all URLs are valid
        for url in new_reviews:
            assert url.startswith("https://platypus1917.org/category/pr/issue-")
            assert url.endswith("/")
        
        logger.info("\n✅ get_new_reviews() works correctly with real archive!")
        
        return new_reviews
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_database_query_performance(self):
        """
        Test that database queries are efficient (bulk query, not N queries).
        """
        logger.info("=" * 60)
        logger.info("Testing Database Query Performance")
        logger.info("=" * 60)
        
        scanner = ArchiveScanner(ARCHIVE_URL)
        
        # Time the scan operation
        import time
        start_time = time.time()
        
        result = await scanner.scan_for_new_reviews()
        
        elapsed = time.time() - start_time
        
        logger.info(f"\n⏱️  Scan completed in {elapsed:.2f} seconds")
        logger.info(f"📊 Processed {result['total_count']} review URLs")
        
        # Should be fast even with many URLs (bulk query)
        assert elapsed < 10.0, f"Scan took too long: {elapsed:.2f}s (should be < 10s)"
        
        logger.info(f"\n✅ Performance is good ({elapsed:.2f}s for {result['total_count']} URLs)")
        
        return result
    
    @pytest.mark.asyncio
    @pytest.mark.integration  
    async def test_archive_scanner_output_format(self):
        """
        Test that ArchiveScanner returns data in expected format for RepostingOrchestrator.
        """
        logger.info("=" * 60)
        logger.info("Testing Output Format for RepostingOrchestrator")
        logger.info("=" * 60)
        
        scanner = ArchiveScanner(ARCHIVE_URL)
        
        # Get new reviews as RepostingOrchestrator does
        new_reviews = await scanner.get_new_reviews()
        
        # Verify it's the right type
        assert isinstance(new_reviews, set), \
            f"get_new_reviews() should return Set[str], got {type(new_reviews)}"
        
        # Verify all elements are strings
        for url in new_reviews:
            assert isinstance(url, str), f"URL should be string, got {type(url)}"
        
        # Verify URLs are fully qualified
        for url in new_reviews:
            assert url.startswith("https://"), f"URL should be absolute: {url}"
        
        logger.info(f"\n✅ Output format is correct for RepostingOrchestrator")
        logger.info(f"   - Type: Set[str] ✓")
        logger.info(f"   - Count: {len(new_reviews)}")
        logger.info(f"   - All URLs are absolute ✓")
        
        return new_reviews


async def main():
    """
    Run archive scanner tests manually (without pytest).
    Useful for quick testing during development.
    """
    print("\n" + "=" * 70)
    print("ARCHIVE SCANNER REAL-WORLD INTEGRATION TEST")
    print("=" * 70)
    print(f"\nArchive URL: {ARCHIVE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    test_instance = TestArchiveScannerReal()
    
    try:
        # Test 1: Full scan
        print("\n\n🧪 TEST 1: Full Archive Scan")
        print("-" * 70)
        scan_result = await test_instance.test_archive_scanner_with_real_archive()
        
        # Test 2: get_new_reviews() method
        print("\n\n🧪 TEST 2: get_new_reviews() Method")
        print("-" * 70)
        new_reviews = await test_instance.test_get_new_reviews_convenience_method()
        
        # Test 3: Performance
        print("\n\n🧪 TEST 3: Performance Test")
        print("-" * 70)
        perf_result = await test_instance.test_database_query_performance()
        
        # Test 4: Output format
        print("\n\n🧪 TEST 4: Output Format Validation")
        print("-" * 70)
        output = await test_instance.test_archive_scanner_output_format()
        
        # Summary
        print("\n\n" + "=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        print(f"✅ All tests passed!")
        print(f"\nArchive Statistics:")
        print(f"  Total reviews in archive: {scan_result['total_count']}")
        print(f"  New reviews: {len(scan_result['new_reviews'])}")
        print(f"  Existing in DB: {len(scan_result['existing_reviews'])}")
        
        # Save results to file
        output_file = "tests/archive_scanner_test_results.json"
        results = {
            "timestamp": datetime.now().isoformat(),
            "archive_url": ARCHIVE_URL,
            "total_reviews": scan_result['total_count'],
            "new_reviews_count": len(scan_result['new_reviews']),
            "existing_reviews_count": len(scan_result['existing_reviews']),
            "new_review_urls": sorted(list(scan_result['new_reviews'])),
            "existing_review_urls": sorted(list(scan_result['existing_reviews']))[:10],  # First 10
            "tests_passed": True
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Results saved to: {output_file}")
        print("=" * 70)
        print("\n✅ SUCCESS: All archive scanner tests passed!\n")
        
        return 0
        
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\n❌ FAILED: Archive scanner tests failed\n")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
