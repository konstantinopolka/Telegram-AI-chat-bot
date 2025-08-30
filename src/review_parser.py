from typing import List, Optional, Dict
import requests
from bs4 import BeautifulSoup


class ReviewParser:
    def __init__(self, base_url: str):
        self.base_url = base_url
        pass
    
    @staticmethod
    def parse_review_page(review_html):
        """Parse review page HTML to extract article URLs"""
        soup = BeautifulSoup(review_html, 'html.parser')
        article_urls = []

        # Extract article links from the listing page
        links = soup.select('h4 > a[href^="https://platypus1917.org/20"]')  # Links starting "https://platypus1917.org/20"
        for link in links:
            href = link.get('href')
            if href:
                if href.startswith('/'):
                    href = 'https://platypus1917.org' + href
                article_urls.append(href)
        
        return article_urls  
    
    @staticmethod
    def _clean_html_for_telegraph(self, content_div) -> str:
        """Clean HTML content for Telegraph compatibility"""
        # Create a copy to avoid modifying original
        content_copy = BeautifulSoup(str(content_div), 'html.parser')
        
        allowed_tags = {
            'a', 'b', 'i', 'em', 'strong', 'u', 's', 'blockquote',
            'code', 'pre', 'p', 'ul', 'ol', 'li', 'br', 'hr', 'img'
        }
        
        # Remove unwanted elements first
        for unwanted in content_copy.select('nav, footer, .sidebar, script, style, .comments'):
            unwanted.decompose()
        
        # Clean tags
        for tag in content_copy.find_all():
            if tag.name not in allowed_tags:
                tag.unwrap()
        
        return ''.join(str(child) for child in content_copy.contents)  