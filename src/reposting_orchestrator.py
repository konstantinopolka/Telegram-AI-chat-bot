#standard libraries
from typing import List, Dict, Any

#third party libraries
from sqlalchemy.ext.asyncio import AsyncSession

#local
from src.scraping.review_scraper import ReviewScraper
from src.telegraph_manager import TelegraphManager
from src.dao.models import Review, Article
from src.logging_config import get_logger
from src.dao import article_repository, review_repository
from src.article_factory import article_factory
from src.channel_poster import ChannelPoster

logger = get_logger(__name__)


class RepostingOrchestrator:
    def __init__(self, review_scraper: ReviewScraper, telegraph_manager: TelegraphManager, db_session, bot_handler, channel_poster):
        self.scraper: ReviewScraper  = review_scraper
        self.telegraph: TelegraphManager = telegraph_manager
        self.db: AsyncSession = db_session
        self.bot = bot_handler
        self.channel_poster: ChannelPoster = channel_poster

    async def process_review_batch(self) -> Review:
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
                articles=processed_articles,
                created_at=raw_review_data.get('created_at')
            )
            #4. Save review in database 
            review = review_repository.add(review)
            
            
            logger.info(f"Batch processing complete. Processed {len(processed_articles)} articles")
            return review
            
        except Exception as e:
            logger.error(f"Error in batch processing: {e}", exc_info=True)
            return None



    async def process_articles(self, raw_review_data: Dict[str, Any]) -> List[Article]:
        """
        Process multiple articles by calling process_single_article for each one.
        """
        
        # Create article schemas from raw data and add them
        logger.info("Step 2: Creating validated article schemas")
        articles: List[Article] = article_factory.from_scraper_data(raw_review_data)
        for article in articles:
            article = article_repository.add(article)
        
        for article in articles:
            try:
                article: Article = await self.process_single_article(article)
                    
            except Exception as e:
                logger.error(f"Error processing article '{article.title}': {e}", exc_info=True)
                continue
        
        return articles

    async def process_single_article(self, article: Article) -> Article:
        """
        Process a single article with validated schema:
        1. Create Telegraph article
        2. Save to DB
        """
        try:
            # 1. Check article_schema
            if not article:
                logger.warning("No article schema provided")
                return None
            
            # 3. Create Telegraph article
            logger.info(f"Creating Telegraph article for '{article.title}'")
            telegraph_urls = await self.telegraph.create_telegraph_articles(article)
            
            if telegraph_urls:
                # Update the article with telegraph URLs
                article.telegraph_urls = telegraph_urls
                # 4. Save to database
                logger.debug("Saving to database")
                article = article_repository.update_telegraph_urls(article.id, telegraph_urls)
                return article
            else:
                logger.warning("Failed to create Telegraph article")
                return None
                
        except Exception as e:
            logger.error(f"Error processing single article '{article.title if article else 'Unknown'}': {e}", exc_info=True)
            return None