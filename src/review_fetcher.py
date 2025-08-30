from typing import List, Optional, Dict, Any

import requests
from bs4 import BeautifulSoup
from src.review_parser import ReviewParser


from telegraph import Telegraph
import json
import os

# ARTICLE_URL = 'https://platypus1917.org/2025/07/01/what-is-capitalism/'
class ReviewFetcher:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.parser = ReviewParser(base_url)
        self.session = requests.Session()  # Reuse connections
        
    # ===============================
    # FETCHING FUNCTIONS - Network operations
    # ===============================

    def fetch_page(self, url: str) -> str:
        """Fetch raw HTML content from a URL"""
        response = self.session.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    
    def fetch_multiple_pages(self, urls: List[str]) -> Dict[str, str]:
        """Fetch multiple pages and return URL -> HTML mapping"""
        results = {}
        for url in urls:
            try:
                html = self.fetch_page(url)
                results[url] = html
            except Exception as e:
                self.handle_request_error(e, url)
        return results
    
    def get_listing_urls(self) -> List[str]:
        """Get article URLs from review listing page"""
        html = self.fetch_page(self.base_url)
        return self.parser.parse_listing_page(html)
    
    def get_content_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Complete workflow: fetch article and parse its content"""
        try:
            html = self.fetch_page(url)
            return self.parser.parse_content_page(html, url)
        except Exception as e:
            self.handle_request_error(e, url)
            return None
    
    def handle_request_error(self, error: Exception, url: str) -> None:
        """Custom error handling for review fetching"""
        print(f"Failed to fetch review from {url}: {error}")
    
    

    

# --- Scrape article ---
response = requests.get(ARTICLE_URL)
soup = BeautifulSoup(response.content, 'html.parser')

title_tag = soup.find('h1')
title = title_tag.get_text(strip=True) if title_tag else "Untitled"

content_div = soup.find('div', class_='dc-page-seo-wrapper')
if not content_div:
    content_div = soup

# Allowed tags
allowed_tags = {'a', 'b', 'i', 'em', 'strong', 'u', 's', 'blockquote',
                'code', 'pre', 'p', 'ul', 'ol', 'li', 'br', 'hr', 'img'}

# Clean HTML: unwrap unallowed tags
for tag in content_div.find_all():
    if tag.name not in allowed_tags:
        tag.unwrap()

# --- Split content safely into chunks ---
MAX_CHARS = 50000
blocks = content_div.find_all(['p', 'ul', 'ol', 'blockquote', 'pre', 'img', 'hr', ])
# print(blocks)
chunks = []
current_chunk = ""

for block in blocks:
    block_html = str(block)
    # If adding this block exceeds the limit, start a new chunk
    if len(current_chunk) + len(block_html) > MAX_CHARS:
        chunks.append(current_chunk)
        current_chunk = block_html
    else:
        current_chunk += block_html

# Add the last chunk
if current_chunk:
    chunks.append(current_chunk)

# --- Create Telegraph pages ---
telegraph_urls = []
for i, chunk in enumerate(chunks):
    print(i)
    print(chunk)
    print(len(chunk))
    page = telegraph.create_page(
        title=title if i == 0 else f"{title} (part {i+1})",
        html_content=chunk,
        author_name="Platypus Review"
    )
    telegraph_urls.append(page['url'])

print("Created Telegraph articles:")
print("\n".join(telegraph_urls))
