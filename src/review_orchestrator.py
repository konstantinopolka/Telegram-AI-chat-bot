#standard libraries
from typing import List, Dict, Any

#third party libraries

#local
from src.scraping.review_scraper import ReviewScraper
from src.telegraph_manager import TelegraphManager
from src.dao.models import Review, Article
from src.logging_config import get_logger
from src.dao import article_repository, review_repository
from src.article_factory import article_factory

logger = get_logger(__name__)


class ReviewOrchestrator:
    def __init__(self, review_scraper: ReviewScraper, telegraph_manager: TelegraphManager = None):
        """
        Initialize the ReviewOrchestrator.
        
        Args:
            review_scraper: ReviewScraper instance for scraping review data
            telegraph_manager: TelegraphManager instance. If None, uses singleton instance.
        """
        self.scraper: ReviewScraper = review_scraper
        # Use provided instance or fall back to singleton
        if telegraph_manager is None:
            from src.telegraph_manager import telegraph_manager as singleton_instance
            self.telegraph_manager = singleton_instance
        else:
            self.telegraph_manager = telegraph_manager

    async def process_review_batch(self) -> tuple[Review, bool]:
        """
        Full workflow for processing a batch of reviews:
        1. Scrape articles data from review site
        2. Create articles from raw data
        3. Process all articles from the scraped review
            3.1 Create Telegraph articles
            3.2 Save articles to data base
            3.3 Post the Telegraph articles to the bot/channel
        4. Create a review out of the articles
        5. Save the review to the data base
        """
        try:
            # 1. Scrape all articles from review site
            logger.info("Step 1: Scraping articles from review site")
            raw_review_data: Dict[str, Any] = self.scraper.scrape_review_batch()
            
            if not raw_review_data:
                logger.warning("No articles found to process")
                return None
            

     
            # 3. Process all articles
            logger.info("Step 4: Processing all articles")
            processed_articles: List[Article] = await self.process_articles(raw_review_data)
            
            
            # 3. Create review
            review = Review(
                id=raw_review_data.get('review_id'),
                source_url=raw_review_data['source_url'],
                articles=processed_articles
            )
            #4. Save review in database 
            review, was_created = await review_repository.save_if_not_exists(review)
            status = "created" if was_created else "already exists"
            logger.info(f"Review {review.id} {status}")
            
            
            
            logger.info(f"Batch processing complete. Processed {len(processed_articles)} articles")
            return review, was_created
            
        except Exception as e:
            logger.error(f"Error in batch processing: {e}", exc_info=True)
            return None



    async def process_articles(self, raw_review_data: Dict[str, Any]) -> List[Article]:
        """
        Process multiple articles by calling process_single_article for each one.
        """
        
        # Create article schemas from raw data
        logger.info("Step 2: Creating validated article schemas")
        articles: List[Article] = article_factory.from_scraper_data(raw_review_data)
        
        # Save articles to database first
        logger.info("Step 3: Saving articles to database")
        saved_articles: List[Article] = []
        for article in articles:
            try:
                saved_article, was_created = await article_repository.save_if_not_exists(article)
                saved_articles.append(saved_article)
                status = "created" if was_created else "already exists"
                logger.debug(f"Saved article ID: {saved_article.id} ({status})")
            except Exception as e:
                logger.error(f"Error saving article '{article.title}': {e}", exc_info=True)
                continue
        
        # Process each article (create Telegraph pages, update with URLs)
        logger.info("Step 4: Processing articles (creating Telegraph pages)")
        for article in saved_articles:
            try:
                await self.process_single_article(article)
            except Exception as e:
                logger.error(f"Error processing article '{article.title}': {e}", exc_info=True)
                continue
        
        return saved_articles

    async def process_single_article(self, article: Article) -> Article:
        """
        Process a single article with validated schema:
        1. Create Telegraph article
        2. Update article in DB with Telegraph URLs
        """
        try:
            # 1. Check article_schema
            if not article:
                logger.warning("No article schema provided")
                return None
            
            # 2. Create Telegraph article
            logger.info(f"Creating Telegraph article for '{article.title}'")
            telegraph_urls = await self.telegraph_manager.create_telegraph_articles(article)

            if telegraph_urls:
                # 3. Update the article with telegraph URLs
                logger.debug("Updating article with Telegraph URLs")
                updated_article = await article_repository.update_telegraph_urls(article.id, telegraph_urls)
                logger.info(f"Successfully processed article: {article.title}")
                return updated_article
            else:
                logger.warning("Failed to create Telegraph article")
                return None
                
        except Exception as e:
            logger.error(f"Error processing single article '{article.title if article else 'Unknown'}': {e}", exc_info=True)
            return None
