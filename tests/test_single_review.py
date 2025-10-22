"""
Integration test for processing a single review end-to-end.

This test covers the complete workflow:
1. Scraping a review and its articles
2. Creating Article instances from scraped data
3. Creating Telegraph articles
4. Saving articles to database
5. Creating and saving a Review with associated articles

Note: Telegram bot posting is not yet implemented, so step 5 (posting) is skipped.
"""

import pytest
import asyncio
import os
from typing import List, Dict, Any

# Local imports
from src.scraping.review_scraper import ReviewScraper
from src.telegraph_manager import TelegraphManager
from src.article_factory import article_factory
from src.dao.models import Article, Review
from src.dao.repositories.article_repository import article_repository
from src.dao.repositories.review_repository import review_repository
from src.dao.core.database_manager import db_manager
from src.logging_config import get_logger

logger = get_logger(__name__)

# Test configuration - easily changeable
TEST_REVIEW_URL = "https://platypus1917.org/category/pr/issue-173/"


class TestSingleReviewWorkflow:
    """Integration test for complete single review processing workflow"""
    
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
        Test the complete workflow for processing a single review.
        
        Workflow steps:
        1. Scrape review and articles from TEST_REVIEW_URL
        2. Create Article instances using ArticleFactory
        3. Create Telegraph articles for each article
        4. Save articles to database
        5. Create Review instance with all articles
        6. Save Review to database
        """
        logger.info("=" * 80)
        logger.info("STARTING COMPLETE REVIEW WORKFLOW TEST")
        logger.info(f"Test URL: {TEST_REVIEW_URL}")
        logger.info("=" * 80)
        
        # ============================================================
        # STEP 1: Scrape review and articles
        # ============================================================
        logger.info("\n" + "=" * 60)
        logger.info("STEP 1: SCRAPING REVIEW AND ARTICLES")
        logger.info("=" * 60)
        
        scraper = ReviewScraper(TEST_REVIEW_URL)
        raw_review_data: Dict[str, Any] = scraper.scrape_review_batch()
        
        assert raw_review_data is not None, "Failed to scrape review data"
        assert 'articles' in raw_review_data, "No articles in scraped data"
        assert 'source_url' in raw_review_data, "No source_url in scraped data"
        assert 'review_id' in raw_review_data, "No review_id in scraped data"
        
        articles_count = len(raw_review_data['articles'])
        logger.info(f"✓ Scraped {articles_count} articles")
        logger.info(f"✓ Review ID: {raw_review_data['review_id']}")
        logger.info(f"✓ Source URL: {raw_review_data['source_url']}")
        
        assert articles_count > 0, "No articles were scraped"
        
        # ============================================================
        # STEP 2: Create Article instances from scraped data
        # ============================================================
        logger.info("\n" + "=" * 60)
        logger.info("STEP 2: CREATING ARTICLE INSTANCES")
        logger.info("=" * 60)
        
        articles: List[Article] = article_factory.from_scraper_data(raw_review_data)
        
        assert articles is not None, "Failed to create articles"
        assert len(articles) == articles_count, f"Expected {articles_count} articles, got {len(articles)}"
        
        logger.info(f"✓ Created {len(articles)} Article instances")
        for i, article in enumerate(articles, 1):
            logger.info(f"  Article {i}: {article.title[:50]}...")
            assert article.title, f"Article {i} has no title"
            assert article.content, f"Article {i} has no content"
            assert article.original_url, f"Article {i} has no original_url"
        
        # ============================================================
        # STEP 3: Create Telegraph articles (optional - requires token)
        # ============================================================
        logger.info("\n" + "=" * 60)
        logger.info("STEP 3: CREATING TELEGRAPH ARTICLES")
        logger.info("=" * 60)
        
        telegraph_token = os.getenv('TELEGRAPH_ACCESS_TOKEN')
        if telegraph_token and telegraph_token != "test_token":
            logger.info("Telegraph token found - creating Telegraph articles")
            telegraph_manager = TelegraphManager(access_token=telegraph_token)
            
            for i, article in enumerate(articles, 1):
                try:
                    logger.info(f"Creating Telegraph article {i}/{len(articles)}: {article.title[:50]}...")
                    telegraph_urls = await telegraph_manager.create_telegraph_articles(article)
                    
                    if telegraph_urls:
                        article.telegraph_urls = telegraph_urls
                        logger.info(f"  ✓ Created {len(telegraph_urls)} Telegraph page(s)")
                        for j, url in enumerate(telegraph_urls, 1):
                            logger.info(f"    Part {j}: {url}")
                    else:
                        logger.warning(f"  ✗ Failed to create Telegraph article for: {article.title[:50]}")
                except Exception as e:
                    logger.error(f"  ✗ Error creating Telegraph article: {e}", exc_info=True)
        else:
            logger.info("⚠ Skipping Telegraph creation - no access token configured")
            logger.info("  Set TELEGRAPH_ACCESS_TOKEN environment variable to enable")
        
        # ============================================================
        # STEP 4: Save articles to database
        # ============================================================
        logger.info("\n" + "=" * 60)
        logger.info("STEP 4: SAVING ARTICLES TO DATABASE")
        logger.info("=" * 60)
        
        saved_articles: List[Article] = []
        for i, article in enumerate(articles, 1):
            try:
                logger.info(f"Saving article {i}/{len(articles)}: {article.title[:50]}...")
                saved_article = await article_repository.save(article)
                saved_articles.append(saved_article)
                
                assert saved_article.id is not None, f"Article {i} was not assigned an ID"
                logger.info(f"  ✓ Saved with ID: {saved_article.id}")
            except Exception as e:
                logger.error(f"  ✗ Failed to save article {i}: {e}", exc_info=True)
                raise
        
        assert len(saved_articles) == len(articles), "Not all articles were saved"
        logger.info(f"✓ Successfully saved {len(saved_articles)} articles to database")
        
        # ============================================================
        # STEP 5: Create and save Review
        # ============================================================
        logger.info("\n" + "=" * 60)
        logger.info("STEP 5: CREATING AND SAVING REVIEW")
        logger.info("=" * 60)
        
        review = Review(
            id=raw_review_data.get('review_id'),
            source_url=raw_review_data['source_url'],
            articles=saved_articles,
            created_at=raw_review_data.get('created_at')
        )
        
        logger.info(f"Created Review instance:")
        logger.info(f"  ID: {review.id}")
        logger.info(f"  Source URL: {review.source_url}")
        logger.info(f"  Articles: {len(review.articles)}")
        
        saved_review = await review_repository.save(review)
        
        assert saved_review.id is not None, "Review was not assigned an ID"
        logger.info(f"✓ Saved Review with ID: {saved_review.id}")
        
        # ============================================================
        # STEP 6: Verify saved data
        # ============================================================
        logger.info("\n" + "=" * 60)
        logger.info("STEP 6: VERIFYING SAVED DATA")
        logger.info("=" * 60)
        
        # Verify review can be retrieved with articles
        retrieved_review = await review_repository.get_with_articles(saved_review.id)
        
        assert retrieved_review is not None, "Failed to retrieve saved review"
        assert retrieved_review.id == saved_review.id, "Retrieved review ID mismatch"
        assert retrieved_review.source_url == TEST_REVIEW_URL, "Retrieved review URL mismatch"
        assert len(retrieved_review.articles) == len(saved_articles), "Article count mismatch"
        
        logger.info(f"✓ Successfully retrieved review from database")
        logger.info(f"  Review ID: {retrieved_review.id}")
        logger.info(f"  Articles: {len(retrieved_review.articles)}")
        
        # Verify individual articles
        for i, article in enumerate(retrieved_review.articles, 1):
            assert article.id is not None, f"Article {i} has no ID"
            assert article.title, f"Article {i} has no title"
            assert article.content, f"Article {i} has no content"
            logger.info(f"  Article {i}: ID={article.id}, Title={article.title[:40]}...")
        
        # ============================================================
        # TEST COMPLETE
        # ============================================================
        logger.info("\n" + "=" * 80)
        logger.info("TEST COMPLETED SUCCESSFULLY!")
        logger.info("=" * 80)
        logger.info(f"Summary:")
        logger.info(f"  - Review ID: {saved_review.id}")
        logger.info(f"  - Articles processed: {len(saved_articles)}")
        logger.info(f"  - Telegraph articles created: {sum(1 for a in saved_articles if a.telegraph_urls)}")
        logger.info(f"  - All data verified in database: ✓")
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
