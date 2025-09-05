from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .constants import REQUIRED_FIELDS
class Scraper(ABC):
    """
    Abstract base class for scrapers that combine fetching and parsing operations.
    A scraper encapsulates the complete workflow of getting content from websites.
    """
    
    @abstractmethod
    def get_listing_urls(self) -> List[str]:
        """
        Get all content URLs from the main listing/index page.
        Returns list of URLs to individual content pages.
        """
        pass
    
    @abstractmethod
    def scrape_single_article(self, article_url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a single article by URL.
        Complete workflow: fetch → parse → validate → return article data.
        Returns dictionary with title, content, metadata, etc.
        """
        pass
    
    @abstractmethod
    def scrape_review_batch(self) -> List[Dict[str, Any]]:
        """
        Scrape a batch of reviews/articles from the main page.
        This is the main method that orchestrates the full scraping process.
        Returns list of structured content data dictionaries.
        """
        pass
    
    # Optional: methods that might have default implementations
    def validate_content_data(self, content_data: Dict[str, Any]) -> bool:
        """
        Validate that content data has required fields.
        Can be overridden for specific validation rules.
        """
        
        return all(field in content_data and content_data[field] for field in REQUIRED_FIELDS)
    
    def handle_scraping_error(self, error: Exception, context: str) -> None:
        """
        Handle scraping errors - can be overridden for custom error handling.
        """
        print(f"Scraping error in {context}: {error}")
