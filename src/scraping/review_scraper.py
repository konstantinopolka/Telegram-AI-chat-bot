from typing import List, Optional, Dict, Any
from .scraper import Scraper
from .fetcher import Fetcher
from .review_parser import ReviewParser
from .constants import MIN_TITLE_LENGTH, MIN_CONTENT_LENGTH
from src.logging_config import get_logger

logger = get_logger(__name__)


class ReviewScraper(Scraper):
    """
    Concrete scraper for review websites that combines fetching and parsing.
    Encapsulates the complete workflow of scraping review articles.
    """
    
    def __init__(self, base_url: str):
        logger.info(f"Initializing ReviewScraper for: {base_url}")
<<<<<<< Updated upstream
        self.base_url = base_url
        self.fetcher = ReviewFetcher(base_url)
        self.parser = ReviewParser(base_url)
=======
        self.base_url: str = base_url
        self.fetcher: Fetcher = Fetcher(base_url)
        self.parser: ReviewParser = ReviewParser(base_url)
>>>>>>> Stashed changes
        logger.debug(f"ReviewScraper initialized with fetcher and parser")
        

    
    def get_listing_urls(self) -> List[str]:
        """
        Get all article URLs from the review listing page.
        """
        logger.info(f"Fetching listing URLs from: {self.base_url}")
        try:
            logger.debug("Fetching HTML from listing page")
            html = self.fetcher.fetch_page()
            logger.debug(f"Received HTML content: {len(html)} characters")
            
            logger.debug("Parsing listing page for article URLs")
            urls = self.parser.parse_listing_page(html)
            logger.info(f"Found {len(urls)} article URLs on listing page")
            return urls
        except Exception as e:
            self.handle_scraping_error(e, "getting listing URLs")
            return []
    
    def get_content_data(self, article_url: str) -> Optional[Dict[str, Any]]:
        """
        Get content data for a single article URL.
        Handles URL validation, fetching, and parsing.
        """
        logger.debug(f"Getting content data for: {article_url}")
        
        # Validate URL format first
        if not self.fetcher.validate_url(article_url):
            logger.warning(f"Invalid URL format: {article_url}")
            return None
        
        logger.debug("URL validated successfully")
        
        # Fetch and parse content
        logger.debug("Fetching HTML content")
        html: str = self.fetcher.fetch_page(article_url)
        logger.debug(f"Received {len(html)} characters of HTML")
        
        logger.debug("Parsing content page")
        content_data = self.parser.parse_content_page(html, article_url)
        logger.debug(f"Extracted content: title='{content_data.get('title', 'N/A')[:50]}...', content_length={len(content_data.get('content', ''))}")
        
        return content_data

    def get_review_id(self) -> Optional[int]:
        """Get review ID, returns None if extraction fails"""
        logger.info("Extracting review ID from base URL")
        try:
            logger.debug(f"Fetching HTML from: {self.base_url}")
            html = self.fetcher.fetch_page()
            
            logger.debug("Parsing review ID from HTML")
            review_id: int = self.parser.extract_review_id(html)
            logger.info(f"Extracted review ID: {review_id}")
            return review_id
        except Exception as e:
            self.handle_scraping_error(e, "getting review ID")
            return None
    
    def scrape_single_article(self, article_url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a single article by URL.
        Complete workflow: fetch → parse → validate → return article data.
        
        Returns:
            Dict with keys:
                - title (str): Article title
                - content (str): Cleaned HTML content
                - original_url (str): Source URL
                - authors (List[str]): List of author names
                - publication_date (str): Publication date
        """
        try:
            logger.info(f"Scraping article: {article_url}")
            
            # 1.2.1 Get page data
            content_data: Dict[str, Any] = self.get_content_data(article_url)
            
            # 1.2.2 Validate content
            if content_data and self.validate_content_data(content_data):
                logger.info(f"Successfully scraped: {content_data['title']}")
                # 1.2.3 Return dictionary representing an article
                return content_data
            else:
                logger.warning(f"Failed to scrape valid content from {article_url}")
                return None
                
        except Exception as e:
            self.handle_scraping_error(e, f"scraping single article {article_url}")
            return None
        
    def scrape_review_batch(self) -> Dict[str, Any]:
        """
        Main scraping method: scrape all review articles.
        Workflow:
        1. Get URLs of each article
        2. Scrape each article (using scrape_single_article)
        3. Return list of dictionaries representing review as a list of articles
        """
        try:
            logger.info(f"Starting review batch scraping from {self.base_url}")
            logger.info("=" * 60)
            
            # 1.1 Get the id of a review
            logger.info("Step 1/4: Extracting review ID")
            review_id: int = self.get_review_id()
            logger.info(f"Review ID: {review_id}")
            
            # 1.2 Get URLs of each article
            logger.info("Step 2/4: Getting article URLs from listing page")
            article_urls: List[str] = self.get_listing_urls()
            if not article_urls:
                logger.warning("No article URLs found on listing page")
                return []
            
            logger.info(f"Found {len(article_urls)} articles to scrape")
            logger.debug(f"Article URLs: {article_urls}")
            
            # 1.3 Scrape each article
            logger.info("Step 3/4: Scraping individual articles")
            scraped_articles: List[Dict[str, Any]] = []
            for idx, url in enumerate(article_urls, 1):
                logger.info(f"Processing article {idx}/{len(article_urls)}: {url}")
                article_data: Dict[str, Any] = self.scrape_single_article(url)
                if article_data:
                    scraped_articles.append(article_data)
                    logger.debug(f"Article {idx} scraped successfully")
                else:
                    logger.warning(f"Article {idx} failed to scrape")
            
            logger.info(f"Step 4/4: Finalizing batch scraping")
            logger.info(f"Successfully scraped {len(scraped_articles)}/{len(article_urls)} articles")
            
            # 1.4 Return a dictionary representing review as a list of articles
            result = {
                "source_url": self.base_url,
                "articles" : scraped_articles,
                "review_id": review_id
            }
            logger.info("=" * 60)
            logger.info(f"Review batch scraping complete: {len(scraped_articles)} articles")
            return result
            
        except Exception as e:
            self.handle_scraping_error(e, "review batch scraping")
            return []
    
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
        logger.error(f"ReviewScraper error in {context}: {error}", exc_info=True)
        # metrics.increment('scraping_errors', tags={'context': context})
        # logger.error(error_msg)
        
        # Could add metrics/monitoring here
        # metrics.increment('scraping_errors', tags={'context': context})
