from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.scraping.constants import REQUIRED_FIELDS 

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
    def get_page_data(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Get structured data from a single content URL.
        Returns dictionary with title, content, metadata, etc.
        """
        pass
    
    @abstractmethod
    def get_multiple_pages_data(self) -> List[Dict[str, Any]]:
        """
        Complete workflow: get all content from the site.
        Returns list of structured content data dictionaries.
        """
        pass
    
    @abstractmethod
    def scrape_review_batch(self) -> List[Dict[str, Any]]:
        """
        Scrape a batch of reviews/articles from the main page.
        This is the main method that orchestrates the full scraping process.
        """
        pass
    
    # Optional: methods that might have default implementations
    def validate_content_data(self, content_data: Dict[str, Any]) -> bool:
        """
        Validate that content data has required fields.
        Can be overridden for specific validation rules.
        """
        REQUIRED_FIELDS = ['title', 'content', 'original_url']
        return all(field in content_data and content_data[field] for field in REQUIRED_FIELDS)
    
    def filter_content_by_criteria(self, content_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter content based on specific criteria.
        Can be overridden for custom filtering logic.
        """
        return [content for content in content_list if self.validate_content_data(content)]
    
    def handle_scraping_error(self, error: Exception, context: str) -> None:
        """
        Handle scraping errors - can be overridden for custom error handling.
        """
        print(f"Scraping error in {context}: {error}")
