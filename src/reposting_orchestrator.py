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
        2. Create Telegraph articles
        3. Save metadata to DB
        4. Post to channel
        """
        try:
            # 1. Scrape all articles from review site
            print("Step 1: Scraping articles from review site...")
            articles_data = self.scraper.scrape_review_batch()
            
            if not articles_data:
                print("No articles found to process")
                return []
            
            processed_articles = []
            
            # 2. Process each article
            for article_data in articles_data:
                try:
                    # Create Telegraph article(s)
                    print(f"Step 2: Creating Telegraph article for '{article_data['title']}'...")
                    telegraph_urls = await self.telegraph.create_article(article_data)
                    
                    if telegraph_urls:
                        # Add Telegraph URLs to article data
                        article_data['telegraph_urls'] = telegraph_urls
                        
                        # 3. Save to database
                        print("Step 3: Saving to database...")
                        # TODO: Save Article object to database
                        # article_obj = Article(**article_data)
                        # self.db.add(article_obj)
                        # self.db.commit()
                        
                        # 4. Post to channel
                        print("Step 4: Posting to channel...")
                        # TODO: Post to Telegram channel
                        # await self.channel.post_article(article_data)
                        
                        processed_articles.append(article_data)
                        print(f"Successfully processed: {article_data['title']}")
                    
                except Exception as e:
                    print(f"Error processing article '{article_data.get('title', 'Unknown')}': {e}")
                    continue
            
            print(f"Batch processing complete. Processed {len(processed_articles)} articles.")
            return processed_articles
            
        except Exception as e:
            print(f"Error in batch processing: {e}")
            return []

    async def process_single_article(self, article_url: str) -> Dict[str, Any]:
        """
        Process a single article by URL:
        1. Scrape single article
        2. Create Telegraph article
        3. Save to DB
        4. Post to channel
        """
        try:
            # 1. Scrape single article
            print(f"Scraping single article: {article_url}")
            article_data = self.scraper.scrape_single_article(article_url)
            
            if not article_data:
                print(f"Failed to scrape article from {article_url}")
                return {}
            
            # 2. Create Telegraph article
            print(f"Creating Telegraph article for '{article_data['title']}'...")
            telegraph_urls = await self.telegraph.create_article(article_data)
            
            if telegraph_urls:
                article_data['telegraph_urls'] = telegraph_urls
                
                # 3. Save to database
                print("Saving to database...")
                # TODO: Implement database saving
                
                # 4. Post to channel
                print("Posting to channel...")
                # TODO: Implement channel posting
                
                print(f"Successfully processed single article: {article_data['title']}")
                return article_data
            else:
                print("Failed to create Telegraph article")
                return {}
                
        except Exception as e:
            print(f"Error processing single article {article_url}: {e}")
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
