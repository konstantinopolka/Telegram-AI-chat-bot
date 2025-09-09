from typing import List, Dict, Any
from src.scraping import ReviewScraper
from src.telegraph_manager import TelegraphManager
from src.schemas import ArticleSchema, ReviewSchema

class RepostingOrchestrator:
    def __init__(self, review_scraper: ReviewScraper, telegraph_manager: TelegraphManager, db_session, bot_handler, channel_poster):
        self.scraper = review_scraper
        self.telegraph = telegraph_manager
        self.db = db_session
        self.bot = bot_handler
        self.channel = channel_poster

    async def process_review_batch(self) -> ReviewSchema:
        """
        Full workflow for processing a batch of reviews:
        1. Scrape articles from review site
        2. Process all articles from the scraped review
        """
        try:
            # 1. Scrape all articles from review site
            print("Step 1: Scraping articles from review site...")
            raw_review_data = self.scraper.scrape_review_batch()
            
            if not raw_review_data:
                print("No articles found to process")
                return None
            
            # 2. Convert raw data to validated schema
            print("Step 2: Creating validated review schema...")
            review_schema = ReviewSchema.from_raw_data(raw_review_data)
            
            # 3. Process all articles
            print("Step 3: Processing all articles...")
            processed_articles = await self.process_articles(review_schema.articles)
            
            print(f"Batch processing complete. Processed {len(processed_articles)} articles.")
            return review_schema
            
        except Exception as e:
            print(f"Error in batch processing: {e}")
            return None

    async def process_articles(self, articles: List[ArticleSchema]) -> List[ArticleSchema]:
        """
        Process multiple articles by calling process_single_article for each one.
        """
        processed_articles = []
        
        for article_schema in articles:
            try:
                processed_article = await self.process_single_article(article_schema)
                if processed_article:  # Only add if processing was successful
                    processed_articles.append(processed_article)
                    
            except Exception as e:
                print(f"Error processing article '{article_schema.title}': {e}")
                continue
        
        return processed_articles

    async def process_single_article(self, article_schema: ArticleSchema) -> ArticleSchema:
        """
        Process a single article with validated schema:
        1. Create Telegraph article
        2. Save to DB
        3. Post to channel
        """
        try:
            # 1. Check article_schema
            if not article_schema:
                print(f"No article schema provided")
                return None
            
            # 2. Convert to dict for Telegraph API
            article_data = article_schema.dict()
            
            # 3. Create Telegraph article
            print(f"Creating Telegraph article for '{article_schema.title}'...")
            telegraph_urls = await self.telegraph.create_article(article_data)
            
            if telegraph_urls:
                # Update the schema with telegraph URLs
                article_schema.telegraph_urls = telegraph_urls
                
                # 4. Save to database
                print("Saving to database...")
                # TODO: Save Article object to database
                # article_obj = Article(**article_schema.dict())
                # self.db.add(article_obj)
                # self.db.commit()
                
                # 5. Post to channel
                print("Posting to channel...")
                # TODO: Post to Telegram channel
                # await self.channel.post_article(article_schema.dict())
                
                print(f"Successfully processed single article: {article_schema.title}")
                return article_schema
            else:
                print("Failed to create Telegraph article")
                return None
                
        except Exception as e:
            print(f"Error processing single article '{article_schema.title if article_schema else 'Unknown'}': {e}")
            return None

    async def preview_available_content(self) -> Dict[str, Any]:
        """
        Preview what content is available for scraping without actually scraping it.
        """
        try:
            return self.scraper.preview_content_summary()
        except Exception as e:
            print(f"Error previewing content: {e}")
            return {'error': str(e)}
