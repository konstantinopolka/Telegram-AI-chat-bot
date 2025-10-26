from typing import List, Dict, Any
from datetime import date
from bs4 import BeautifulSoup
from src.scraping.listing_parser import ListingParser
from src.scraping.content_parser import ContentParser

from .constants import ALLOWED_TAGS, IRRELEVANT_INFO_TAGS
from src.logging_config import get_logger
import requests

logger = get_logger(__name__)


class ReviewParser(ListingParser, ContentParser):
    def __init__(self, base_url: str, article_selectors: List[str] = None):
        logger.info(f"Initializing ReviewParser for: {base_url}")
        
        # Default selectors for article links
        default_selectors = [
            'h4 > a[href^="/20"]',
            'h4 > a[href^="https://platypus1917.org/20"]'
        ]
        
        selectors = article_selectors or default_selectors
        ListingParser.__init__(self, base_url=base_url, link_selectors=selectors)
        logger.debug("ReviewParser initialized")
        
    
    def parse_content_page(self, html: str, url: str) -> Dict[str, Any]:
        """Parse single article HTML to extract structured data"""
        logger.debug(f"Parsing content page: {url}")
        logger.debug(f"HTML length: {len(html)} characters")
        
        soup = self.create_soup(html)
        logger.debug("BeautifulSoup object created for content page")
        
        logger.debug("Extracting title")
        title = self.extract_title(soup)
        logger.debug(f"Title extracted: '{title}'")
        
        logger.debug("Extracting content")
        content = self.extract_content(soup)
        logger.debug(f"Content extracted: {len(content)} characters")
        
        logger.debug("Extracting metadata")
        metadata = self.extract_metadata(soup, url)
        logger.debug(f"Metadata extracted: {list(metadata.keys())}")
        
        result = {
            'title': title,
            'content': content,
            'original_url': url,
            **metadata
        }
        logger.info(f"Successfully parsed content page: '{title}' ({len(content)} chars)")
        return result
        
    def extract_metadata(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract metadata from Platypus article"""
        return {
            'authors': self._extract_authors(soup),
            'publication_date': self._extract_date(soup, url),
        }

        
    def extract_review_id(self, html: str) -> int:
        """Extract review ID from HTML span or URL"""
        
        # Method 1: Try HTML span first
        soup = self.create_soup(html)
        span = soup.select_one('span.selected')
        if span:
            text = span.get_text(strip=True)
            import re
            match = re.search(r'Issue #(\d+)', text)
            if match:
                return int(match.group(1))
        
        # Method 2: Fallback to base_url if it contains the pattern
        if hasattr(self, 'base_url') and self.base_url:
            import re
            match = re.search(r'/issue-(\d+)/?', self.base_url)
            if match:
                return int(match.group(1))
        
        # Final fallback
        return hash(self.base_url) % 1000000
    

    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract title from Platypus article"""
        ARTICLE_TITLE_TAG = '.bpf-title'
        
        #Method 1: extract title by class name
        title_tag = soup.select_one(ARTICLE_TITLE_TAG)
        
        #Method 2: extract title by tag
        if title_tag is None: 
            title_tag = soup.select_one('h1')
        
        return self.clean_text(title_tag.get_text()) if title_tag else "Untitled"
    
    def extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from Platypus article"""
        MAIN_CONTENT_TAG_CLASS = 'bpf-content'
        
        content_div = soup.find('div', class_= MAIN_CONTENT_TAG_CLASS)
        if not content_div:
            content_div = soup
        
        return self.clean_content_for_publishing(content_div)
    
    def clean_content_for_publishing(self, content_div) -> str:
        """Clean HTML content for Telegraph compatibility"""
        content_copy = BeautifulSoup(str(content_div), 'html.parser')
        
        # Apply cleaning operations
        self._remove_unwanted_elements(content_copy)
        self._clean_disallowed_tags(content_copy)
        self._wrap_orphaned_inline_elements(content_copy)
        
        return ''.join(str(child) for child in content_copy.contents)
    
    def _remove_unwanted_elements(self, soup: BeautifulSoup) -> None:
        """Remove unwanted elements from the soup"""
        for unwanted in soup.select(IRRELEVANT_INFO_TAGS):
            unwanted.decompose()
    
    def _clean_disallowed_tags(self, soup: BeautifulSoup) -> None:
        """Remove disallowed tags while preserving their content"""
        for tag in soup.find_all():
            if tag.name not in ALLOWED_TAGS:
                tag.unwrap()
                
    def _wrap_orphaned_inline_elements(self, soup: BeautifulSoup) -> None:
        """Wrap orphaned inline elements in paragraph tags"""
        inline_tags = {'strong', 'b', 'i', 'em', 'u', 's', 'a', 'code'}
        
        # Find direct children of the soup that are inline elements
        for element in list(soup.children):
            if (hasattr(element, 'name') and 
                element.name in inline_tags and 
                element.parent == soup):
                
                # Check if there's already a paragraph wrapper
                prev_sibling = element.previous_sibling
                if (prev_sibling and hasattr(prev_sibling, 'name') and 
                    prev_sibling.name == 'p'):
                    # Move this element into the previous paragraph
                    prev_sibling.append(element)
                else:
                    # Create a new paragraph wrapper
                    new_p = soup.new_tag('p')
                    element.insert_before(new_p)
                    new_p.append(element)

    
    def _extract_authors(self, soup: BeautifulSoup) -> List[str]:
        """Extract authors from article"""
        authors = []
        byline = soup.select_one('.bpf-content h2')
        if byline:
            text = byline.get_text(strip=True)  # Keep original case
            
            # Check if it contains "by" prefix
            if 'by ' in text.lower():
                # Extract part after "by"
                author_part = text.split('by ')[1] if 'by ' in text else text.split('By ')[1]
            else:
                # No "by" prefix, use the whole text as authors
                author_part = text
            
            # Split on "and" and clean up
            authors = [a.strip() for a in author_part.replace(' and ', ',').split(',')]
            
        return [a for a in authors if a]
    
    def _extract_date(self, soup: BeautifulSoup, url: str) -> date:
        """
        Extract publication date as a date object.
        
        Args:
            soup: BeautifulSoup object of the article page
            url: Article URL
            
        Returns:
            date object representing publication date
            
        Raises:
            ValueError: If publication date cannot be extracted
        """
        import re
        
        # Method 1: Extract from URL pattern (e.g., /2025/10/01/)
        if (url_match := re.search(r'/(\d{4})/(\d{2})/(\d{2})/', url)):
            year, month, day = map(int, url_match.groups())
            try:
                return date(year, month, day)
            except ValueError as e:
                logger.warning(f"Invalid date from URL: {year}/{month}/{day}: {e}")
        
        # Method 2: Fallback to HTML pattern "| February 2025" or "| July–August 2025"
        if (container := soup.select_one('.bpf-content .has-text-align-right')):
            text = container.get_text(strip=True)
            # Split on "|" and take the date part
            if "|" in text:
                date_part = text.split("|")[1].strip()
                
                # Parse month name and year (e.g., "February 2025" or "July–August 2025")
                # Take first month if range, set day to 1
                if (month_year_match := re.match(r'(\w+)(?:–\w+)?\s+(\d{4})', date_part)):
                    month_name, year = month_year_match.groups()
                    month_map = {
                        'January': 1, 'February': 2, 'March': 3, 'April': 4,
                        'May': 5, 'June': 6, 'July': 7, 'August': 8,
                        'September': 9, 'October': 10, 'November': 11, 'December': 12
                    }
                    if (month_num := month_map.get(month_name)):
                        try:
                            return date(int(year), month_num, 1)
                        except ValueError as e:
                            logger.warning(f"Invalid date from HTML: {year}/{month_num}/1: {e}")
        
        # Final fallback: raise exception as publication_date is required
        error_msg = f"Could not extract publication date from URL: {url}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    


