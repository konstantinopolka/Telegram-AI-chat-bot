from typing import List, Dict, Any
from src.scraping import ReviewScraper
from src.telegraph_manager import TelegraphManager

class RepostingOrchestrator:
    def __init__(self, review_scraper: ReviewScraper, telegraph_manager: TelegraphManager, db_session, bot_handler, channel_poster):
        self.scraper = review_scraper
        self.telegraph = telegraph_manager
        self.db = db_session
        self.bot = bot_handler
        self.channel = channel_poster

    async def process_review_batch(self) -> List[Dict[str, Any]]:
        """
        Full workflow for processing a batch of reviews:
        1. Scrape articles from review site
        2. Process all articles from the scraped review
        """
        try:
            # 1. Scrape all articles from review site
            print("Step 1: Scraping articles from review site...")
            articles_data = self.scraper.scrape_review_batch()
            
            if not articles_data:
                print("No articles found to process")
                return []
            
            # 2. Process all articles
            print("Step 2: Processing all articles...")
            processed_articles = await self.process_articles(articles_data)
            
            print(f"Batch processing complete. Processed {len(processed_articles)} articles.")
            return processed_articles
            
        except Exception as e:
            print(f"Error in batch processing: {e}")
            return []

    async def process_articles(self, articles_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process multiple articles by calling process_single_article for each one.
        """
        processed_articles = []
        
        for article_data in articles_data:
            try:
                processed_article = await self.process_single_article(article_data)
                if processed_article:  # Only add if processing was successful
                    processed_articles.append(processed_article)
                    
            except Exception as e:
                print(f"Error processing article '{article_data.get('title', 'Unknown')}': {e}")
                continue
        
        return processed_articles

    async def process_single_article(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single article with already scraped data:
        1. Create Telegraph article
        2. Save to DB
        3. Post to channel
        """
        try:
            # 1. Check article_data
            if not article_data:
                print(f"No article data provided")
                return {}
            
            # 2. Create Telegraph article
            print(f"Creating Telegraph article for '{article_data['title']}'...")
            telegraph_urls = await self.telegraph.create_article(article_data)
            
            if telegraph_urls:
                article_data['telegraph_urls'] = telegraph_urls
                
                # 3. Save to database
                print("Saving to database...")
                # TODO: Save Article object to database
                # article_obj = Article(**article_data)
                # self.db.add(article_obj)
                # self.db.commit()
                
                # 4. Post to channel
                print("Posting to channel...")
                # TODO: Post to Telegram channel
                # await self.channel.post_article(article_data)
                
                print(f"Successfully processed single article: {article_data['title']}")
                return article_data
            else:
                print("Failed to create Telegraph article")
                return {}
                
        except Exception as e:
            print(f"Error processing single article '{article_data.get('title', 'Unknown')}': {e}")
            return {}

    async def preview_available_content(self) -> Dict[str, Any]:
        """
        Preview what content is available for scraping without actually scraping it.
        """
        try:
            return self.scraper.preview_content_summary()
        except Exception as e:
            print(f"Error previewing content: {e}")
            return {'error': str(e)}
