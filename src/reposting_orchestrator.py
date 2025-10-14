from typing import List, Dict, Any
from src.scraping.review_scraper import ReviewScraper
from src.telegraph_manager import TelegraphManager
from src.dao.models import Review, Article

class RepostingOrchestrator:
    def __init__(self, review_scraper: ReviewScraper, telegraph_manager: TelegraphManager, db_session, bot_handler, channel_poster):
        self.scraper = review_scraper
        self.telegraph = telegraph_manager
        self.db = db_session
        self.bot = bot_handler
        self.channel = channel_poster

    async def process_review_batch(self) -> Review:
        """
        Full workflow for processing a batch of reviews:
        1. Scrape articles from review site
        2. Create validated schemas from raw data
        3. Process all articles from the scraped review
        """
        try:
            # 1. Scrape all articles from review site
            print("Step 1: Scraping articles from review site...")
            raw_review_data: Dict[str, Any] = self.scraper.scrape_review_batch()
            
            if not raw_review_data:
                print("No articles found to process")
                return None
            

     
            # 3. Process all articles
            print("Step 4: Processing all articles...")
            processed_articles: List[Article] = await self.process_articles(raw_review_data)
            
            
            # 4. Create review
            review = Review(
                id=raw_review_data.get('review_id'),
                source_url=raw_review_data['source_url'],
                articles=processed_articles,
                created_at=raw_review_data.get('created_at')
            )
            
            # TO-DO: 3. Save review in database 
            
            
            print(f"Batch processing complete. Processed {len(processed_articles)} articles.")
            return review
            
        except Exception as e:
            print(f"Error in batch processing: {e}")
            return None



    async def process_articles(self, raw_review_data: Dict[str, Any]) -> List[Article]:
        """
        Process multiple articles by calling process_single_article for each one.
        """
        
        # 2. Create article schemas from raw data
        print("Step 2: Creating validated article schemas...")
        articles = self._create_articles(raw_review_data)
        
        for article in articles:
            try:
                article = await self.process_single_article(article)
                    
            except Exception as e:
                print(f"Error processing article '{article.title}': {e}")
                continue
        
        return articles

    async def process_single_article(self, article: Article) -> Article:
        """
        Process a single article with validated schema:
        1. Create Telegraph article
        2. Save to DB
        3. Post to channel
        """
        try:
            # 1. Check article_schema
            if not article:
                print(f"No article schema provided")
                return None
            
            # 3. Create Telegraph article
            print(f"Creating Telegraph article for '{article.title}'...")
            telegraph_urls = await self.telegraph.create_article(article)
            
            if telegraph_urls:
                # Update the schema with telegraph URLs
                article.telegraph_urls = telegraph_urls
                
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
                
                print(f"Successfully processed single article: {article.title}")
                return article
            else:
                print("Failed to create Telegraph article")
                return None
                
        except Exception as e:
            print(f"Error processing single article '{article.title if article else 'Unknown'}': {e}")
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


    def _create_articles(self, raw_review_data: Dict[str, Any]) -> List[Article]:
        """
        Create ArticleSchema instances from raw scraped data.
        
        Args:
            raw_review_data: Dict containing 'articles' list and 'review_id'
            
        Returns:
            List of validated ArticleSchema instances
        """
        articles = []
        review_id = raw_review_data.get('review_id')
        
        for article_dict in raw_review_data.get('articles', []):
            try:
                # Add review_id to each article if not already present
                if 'review_id' not in article_dict:
                    article_dict['review_id'] = review_id
                    
                article_schema = Article(**article_dict)
                articles.append(article_schema)
            except Exception as e:
                print(f"Failed to create article schema: {e}")
                continue
                
        return articles