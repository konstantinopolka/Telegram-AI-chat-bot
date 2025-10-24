"""
Integration test for processing a single review end-to-end using RepostingOrchestrator.

This test covers the complete workflow through the orchestrator:
1. Orchestrator scrapes review and articles
2. Orchestrator creates Article instances
3. Orchestrator saves articles to database
4. Orchestrator creates Telegraph articles
5. Orchestrator creates and saves Review with associated articles

Uses the actual RepostingOrchestrator to test the real workflow.
"""

import pytest
import asyncio
import os
from typing import List
from datetime import date
from unittest.mock import MagicMock

# Local imports
from src.scraping.review_scraper import ReviewScraper
from src.telegraph_manager import TelegraphManager
from src.reposting_orchestrator import RepostingOrchestrator
from src.channel_poster import ChannelPoster
from src.dao.models import Review
from src.dao.repositories.review_repository import review_repository
from src.dao.core.database_manager import db_manager
from src.logging_config import get_logger
from dotenv import load_dotenv

logger = get_logger(__name__)
load_dotenv()

# Test configuration - easily changeable
TEST_REVIEW_URL = "https://platypus1917.org/category/pr/issue-173/"


class TestSingleReviewWorkflow:
    """Integration test for complete single review processing workflow using RepostingOrchestrator"""
    
    @pytest.fixture(autouse=True)
    async def setup_and_teardown(self):
        """Set up test environment and clean up after test"""
        logger.info("=" * 80)
        logger.info("SETTING UP TEST ENVIRONMENT")
        logger.info("=" * 80)
        
        yield
        
        # Cleanup after test
        logger.info("=" * 80)
        logger.info("CLEANING UP TEST ENVIRONMENT")
        logger.info("=" * 80)
        await db_manager.close()
    
    @pytest.mark.asyncio
    async def test_complete_review_workflow(self):
        """
        Test the complete workflow for processing a single review using RepostingOrchestrator.
        
        The orchestrator handles:
        1. Scraping review and articles
        2. Creating Article instances
        3. Saving articles to database
        4. Creating Telegraph articles
        5. Creating and saving Review
        """
        logger.info("=" * 80)
        logger.info("STARTING COMPLETE REVIEW WORKFLOW TEST")
        logger.info(f"Test URL: {TEST_REVIEW_URL}")
        logger.info("=" * 80)
        
        # ============================================================
        # SETUP: Initialize orchestrator dependencies
        # ============================================================
        logger.info("\n" + "=" * 60)
        logger.info("SETUP: INITIALIZING ORCHESTRATOR")
        logger.info("=" * 60)
        
        # Create scraper
        scraper = ReviewScraper(TEST_REVIEW_URL)
        logger.info(f"✓ Created ReviewScraper for: {TEST_REVIEW_URL}")
        
        # Create Telegraph manager (if token available)
        telegraph_token = os.getenv('TELEGRAPH_ACCESS_TOKEN')
        if telegraph_token and telegraph_token != "test_token":
            telegraph_manager = TelegraphManager(access_token=telegraph_token)
            logger.info("✓ Created TelegraphManager with access token")
        else:
            logger.info("⚠ No Telegraph token - using mock TelegraphManager")
            telegraph_manager = TelegraphManager(access_token="test_token")
        
        # Create mock bot handler (not needed for this test)
        bot_handler = MagicMock()
        logger.info("✓ Created mock bot handler")
        
        # Create mock channel poster (not posting in this test)
        channel_poster = ChannelPoster(bot_handler, channel_id=-1)
        logger.info("✓ Created ChannelPoster")
        
        # Create orchestrator
        orchestrator = RepostingOrchestrator(
            review_scraper=scraper,
            telegraph_manager=telegraph_manager,
            bot_handler=bot_handler,
            channel_poster=channel_poster
        )
        logger.info("✓ Created RepostingOrchestrator")
        
        # ============================================================
        # EXECUTE: Run the complete workflow through orchestrator
        # ============================================================
        logger.info("\n" + "=" * 60)
        logger.info("EXECUTING: PROCESSING REVIEW BATCH")
        logger.info("=" * 60)
        
        # Process the entire review batch
        review: Review = await orchestrator.process_review_batch()
        
        # ============================================================
        # VERIFY: Check results
        # ============================================================
        logger.info("\n" + "=" * 60)
        logger.info("VERIFYING: RESULTS")
        logger.info("=" * 60)
        
        # Verify review was created
        assert review is not None, "Orchestrator returned None - workflow failed"
        assert review.id is not None, "Review has no ID"
        assert review.source_url == TEST_REVIEW_URL, "Review URL mismatch"
        
        logger.info("✓ Review created successfully")
        logger.info(f"  Review ID: {review.id}")
        logger.info(f"  Source URL: {review.source_url}")
        
        # Fetch review with articles from database (orchestrator returns detached instance)
        retrieved_review = await review_repository.get_with_articles(review.id)
        assert retrieved_review is not None, "Failed to retrieve review from database"
        assert retrieved_review.articles is not None, "Review has no articles"
        assert len(retrieved_review.articles) > 0, "Review has no articles"
        
        logger.info(f"  Articles: {len(retrieved_review.articles)}")
        
        # Verify articles
        for i, article in enumerate(retrieved_review.articles, 1):
            assert article.id is not None, f"Article {i} has no ID"
            assert article.title, f"Article {i} has no title"
            assert article.content, f"Article {i} has no content"
            assert article.original_url, f"Article {i} has no original_url"
            assert article.publication_date is not None, f"Article {i} has no publication_date"
            assert isinstance(article.publication_date, date), f"Article {i} publication_date is not a date object"
            assert article.review_id == retrieved_review.id, f"Article {i} review_id mismatch"
            
            logger.info(f"  Article {i}: {article.title[:50]}... (ID={article.id}, Date={article.publication_date})")
        
        # Verify data persisted in database
        logger.info("\n" + "=" * 60)
        logger.info("VERIFYING: DATABASE PERSISTENCE")
        logger.info("=" * 60)
        
        retrieved_review = await review_repository.get_with_articles(review.id)
        
        assert retrieved_review is not None, "Failed to retrieve review from database"
        assert retrieved_review.id == review.id, "Retrieved review ID mismatch"
        assert len(retrieved_review.articles) > 0, "No articles in database"
        
        logger.info("✓ Successfully retrieved review from database")
        logger.info(f"  Review ID: {retrieved_review.id}")
        logger.info(f"  Articles in DB: {len(retrieved_review.articles)}")
        
        # Verify Telegraph URLs (if created)
        telegraph_count = sum(1 for a in retrieved_review.articles if a.telegraph_urls)
        logger.info(f"  Articles with Telegraph URLs: {telegraph_count}/{len(retrieved_review.articles)}")
        
        # ============================================================
        # TEST COMPLETE
        # ============================================================
        logger.info("\n" + "=" * 80)
        logger.info("TEST COMPLETED SUCCESSFULLY!")
        logger.info("=" * 80)
        logger.info("Summary:")
        logger.info(f"  - Review ID: {review.id}")
        logger.info(f"  - Articles processed: {len(retrieved_review.articles)}")
        logger.info(f"  - Telegraph articles created: {telegraph_count}")
        logger.info("  - All data verified in database: ✓")
        logger.info("  - Orchestrator workflow: ✓")
        logger.info("=" * 80)


# Standalone execution
if __name__ == "__main__":
    """
    Run the test directly without pytest.
    Usage: python tests/test_single_review.py
    """
    import sys
    
    # Set up Python path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    
    # Run the test
    logger.info("Running test in standalone mode")
    test_instance = TestSingleReviewWorkflow()
    
    async def run_test():
        async for _ in test_instance.setup_and_teardown():
            await test_instance.test_complete_review_workflow()
    
    asyncio.run(run_test())
