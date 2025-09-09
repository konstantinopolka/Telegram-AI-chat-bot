from typing import List, Optional, Dict, Any
from .scraper import Scraper
from .review_fetcher import ReviewFetcher
from .review_parser import ReviewParser
from .constants import MIN_TITLE_LENGTH, MIN_CONTENT_LENGTH
from src.dao.models import Article, Review

class ReviewScraper(Scraper):
    """
    Concrete scraper for review websites that combines fetching and parsing.
    Encapsulates the complete workflow of scraping review articles.
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.fetcher = ReviewFetcher(base_url)
        self.parser = ReviewParser(base_url)
    
    def get_listing_urls(self) -> List[str]:
        """
        Get all article URLs from the review listing page.
        """
        try:
            html = self.fetcher.fetch_page(self.base_url)
            return self.parser.parse_listing_page(html)
        except Exception as e:
            self.handle_scraping_error(e, "getting listing URLs")
            return []
    
    def get_content_data(self, article_url: str) -> Optional[Dict[str, Any]]:
        """
        Get content data for a single article URL.
        Handles URL validation, fetching, and parsing.
        """
        # Validate URL format first
        if not self.fetcher.validate_url(article_url):
            print(f"Invalid URL format: {article_url}")
            return None
        
        # Fetch and parse content
        html = self.fetcher.fetch_page(article_url)
        content_data = self.parser.parse_content_page(html, article_url)
        return content_data

    def scrape_single_article(self, article_url: str) -> Optional[Article]:
        """
        Scrape a single article by URL.
        Complete workflow: fetch → parse → validate → return article data.
        """
        try:
            print(f"Scraping article: {article_url}")
            
            # 1.2.1 Get page data
            content_data = self.get_content_data(article_url)
            
            # 1.2.2 Validate content
            if content_data and self.validate_content_data(content_data):
                print(f"Successfully scraped: {content_data['title']}")
                # 1.2.3 Return dictionary representing an article
                return content_data
            else:
                print(f"Failed to scrape valid content from {article_url}")
                return None
                
        except Exception as e:
            self.handle_scraping_error(e, f"scraping single article {article_url}")
            return None
        
    def scrape_review_batch(self) -> Review:
        """
        Main scraping method: scrape all review articles.
        Workflow:
        1. Get URLs of each article
        2. Scrape each article (using scrape_single_article)
        3. Return list of dictionaries representing review as a list of articles
        """
        try:
            print(f"Starting review batch scraping from {self.base_url}")
            
            # 1.1 Get URLs of each article
            article_urls = self.get_listing_urls()
            if not article_urls:
                print("No article URLs found on listing page")
                return []
            
            print(f"Found {len(article_urls)} articles to scrape")
            
            # 1.2 Scrape each article
            scraped_articles = [article_data for url in article_urls if (article_data := self.scrape_single_article(url))]
            
            print(f"Successfully scraped {len(scraped_articles)} articles")
            # 1.3 Return list of dictionaries representing review as a list of articles
            return scraped_articles
            
        except Exception as e:
            self.handle_scraping_error(e, "review batch scraping")
            return []
    
    def preview_content_summary(self) -> Dict[str, Any]:
        """
        Get a summary of available content without full scraping.
        Useful for previewing what will be scraped.
        """
        try:
            article_urls = self.get_listing_urls()
            return {
                'base_url': self.base_url,
                'total_articles': len(article_urls),
                'article_urls': article_urls[:5],  # First 5 URLs as preview
                'has_more': len(article_urls) > 5
            }
        except Exception as e:
            self.handle_scraping_error(e, "preview content summary")
            return {'error': str(e)}
    
    def validate_content_data(self, content_data: Dict[str, Any]) -> bool:
        """
        Validate content data for review articles.
        Override parent method with review-specific validation.
        """
        # Basic validation from parent class
        if not super().validate_content_data(content_data):
            return False
       
        # Review-specific validation
        if len(content_data.get('title', '')) < MIN_TITLE_LENGTH:
            return False
        
        if len(content_data.get('content', '')) < MIN_CONTENT_LENGTH:
            return False
        
        # Check if content has minimum HTML structure
        if '<p>' not in content_data.get('content', ''):
            return False
        
        return True
    
    def handle_scraping_error(self, error: Exception, context: str) -> None:
        """
        Enhanced error handling for review scraping.
        """
        error_msg = f"ReviewScraper error in {context}: {error}"
        print(error_msg)
        
        # Could add logging here in the future
        # logger.error(error_msg)
        
        # Could add metrics/monitoring here
        # metrics.increment('scraping_errors', tags={'context': context})
        # logger.error(error_msg)
        
        # Could add metrics/monitoring here
        # metrics.increment('scraping_errors', tags={'context': context})
