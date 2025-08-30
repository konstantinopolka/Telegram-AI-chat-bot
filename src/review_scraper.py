from typing import List, Optional, Dict, Any
from src.scraper import Scraper
from src.review_fetcher import ReviewFetcher
from src.review_parser import ReviewParser

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
    
    def get_content_data(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Get structured data from a single article URL.
        Returns dictionary ready for Telegraph publishing.
        """
        try:
            html = self.fetcher.fetch_page(url)
            return self.parser.parse_content_page(html, url)
        except Exception as e:
            self.handle_scraping_error(e, f"getting content from {url}")
            return None
        
    def get_all_content_data(self) -> List[Dict[str, Any]]:
        """
        Complete workflow: get all articles from the review site.
        1. Get listing URLs
        2. Fetch and parse each article
        3. Filter and validate content
        """
        all_content = []
        
        # Get all article URLs from listing page
        article_urls = self.get_listing_urls()
        if not article_urls:
            print("No article URLs found on listing page")
            return []
        
        print(f"Found {len(article_urls)} articles to scrape")
        
        # Fetch and parse each article
        for url in article_urls:
            content_data = self.get_content_data(url)
            if content_data and self.validate_content_data(content_data):
                all_content.append(content_data)
            else:
                print(f"Skipped invalid content from {url}")
        
        return all_content
    
    def scrape_review_batch(self) -> List[Dict[str, Any]]:
        """
        Main scraping method: get all review articles ready for publishing.
        This is the primary interface for the RepostingOrchestrator.
        """
        try:
            print(f"Starting review batch scraping from {self.base_url}")
            
            # Get all content data
            content_list = self.get_all_content_data()
            
            # Apply any additional filtering
            filtered_content = self.filter_content_by_criteria(content_list)
            
            print(f"Successfully scraped {len(filtered_content)} articles")
            return filtered_content
            
        except Exception as e:
            self.handle_scraping_error(e, "review batch scraping")
            return []
    
    def scrape_single_article(self, article_url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a single article by URL.
        Useful for testing or processing specific articles.
        """
        try:
            print(f"Scraping single article: {article_url}")
            
            # Validate URL format
            if not self.fetcher.validate_url(article_url):
                print(f"Invalid URL format: {article_url}")
                return None
            
            # Get content data
            content_data = self.get_content_data(article_url)
            
            if content_data and self.validate_content_data(content_data):
                print(f"Successfully scraped: {content_data['title']}")
                return content_data
            else:
                print(f"Failed to scrape valid content from {article_url}")
                return None
                
        except Exception as e:
            self.handle_scraping_error(e, f"scraping single article {article_url}")
            return None
    
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
        if len(content_data.get('title', '')) < 5:
            return False
        
        if len(content_data.get('content', '')) < 100:
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
