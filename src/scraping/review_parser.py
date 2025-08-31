from typing import List, Dict, Any
from bs4 import BeautifulSoup
from src.scraping.parser import Parser

class ReviewParser(Parser):
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    def parse_listing_page(self, html: str) -> List[str]:
        """Parse review page HTML to extract article URLs"""
        soup = self.create_soup(html)
        article_urls = []

        links = soup.select('h4 > a[href^="https://platypus1917.org/20"]')
        for link in links:
            href = link.get('href')
            if href:
                url = self.normalize_url(href, self.base_url)
                article_urls.append(url)
        
        return article_urls
    
    def parse_content_page(self, html: str, url: str) -> Dict[str, Any]:
        """Parse single article HTML to extract structured data"""
        soup = self.create_soup(html)
        #TO-DO
        # required_fields = ['title', 'content', 'original_url']
        
        return {
            'title': self.extract_title(soup),
            'content': self.extract_content(soup),
            'original_url': url,
            **self.extract_metadata(soup),
            'review_id': hash(url) % 1000000
        }
    
    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract title from Platypus article"""
        title_tag = soup.select_one('h1')
        return self.clean_text(title_tag.get_text()) if title_tag else "Untitled"
    
    def extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from Platypus article"""
        content_div = soup.find('div', class_='dc-page-seo-wrapper')
        if not content_div:
            content_div = soup
        
        return self.clean_content_for_publishing(content_div)
    
    def extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        #TO-DO
        
        """Extract metadata from Platypus article"""
        metadata = {
            'authors': self._extract_authors(soup),
            'published_date': self._extract_date(soup)
        }
        return metadata
    
    def clean_content_for_publishing(self, content_div) -> str:
        """Clean HTML content for Telegraph compatibility"""
        content_copy = BeautifulSoup(str(content_div), 'html.parser')
        
        allowed_tags = {
            'a', 'b', 'i', 'em', 'strong', 'u', 's', 'blockquote',
            'code', 'pre', 'p', 'ul', 'ol', 'li', 'br', 'hr', 'img'
        }
        
        # Remove unwanted elements
        for unwanted in content_copy.select('nav, footer, .sidebar, script, style, .comments'):
            unwanted.decompose()
        #TO-DO
        
        # Clean tags
        for tag in content_copy.find_all():
            if tag.name not in allowed_tags:
                tag.unwrap()
        
        return ''.join(str(child) for child in content_copy.contents)
    
    def _extract_authors(self, soup: BeautifulSoup) -> List[str]:
        """Extract authors from article"""
        #TO-DO
        
        authors = []
        byline = soup.select_one('.bpf-content h2')
        if byline:
            text = byline.get_text(strip=True).lower()
            if 'by ' in text:
                author_part = text.split('by ')[1]
                authors = [a.strip() for a in author_part.replace(' and ', ',').split(',')]
        return [a for a in authors if a]
    
    def _extract_date(self, soup: BeautifulSoup) -> str:
        """Extract publication date"""
        
        #TO-DO
        date_elem = soup.select_one('time, .date, [class*="date"]')
        if date_elem:
            return date_elem.get('datetime') or self.clean_text(date_elem.get_text())
        return ""