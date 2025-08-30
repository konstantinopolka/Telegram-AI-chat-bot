from typing import List, Optional, Dict

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
        
        
    # ===============================
    # FETCHING FUNCTIONS - Network operations
    # ===============================

    def fetch_review_page(self) -> List[str]:
        """Fetch raw HTML from review listing page"""
        response = requests.get(self.base_url)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.text
    
    def get_article_urls(self) -> List[str]:
        """Complete workflow: fetch review page and parse article URLs"""
        html = self.fetch_review_page()
        return ReviewParser.parse_review_page(html)

    async def fetch_article_html(self, article_url: str) -> Optional[str]:
        """Fetch raw HTML content from a single article URL"""
        try:
            response = requests.get(article_url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Failed to fetch {article_url}: {e}")
            return None
    
    
    def fetch_multiple_articles(self, urls: List[str]) -> Dict[str, str]:
        """Fetch multiple articles and return URL -> HTML mapping"""
        results = {}
        for url in urls:
            html = self.fetch_article_html(url)
            if html:
                results[url] = html
        return results
    

    
    

    async def parse_article_html(self, html: str) -> str:
        """
        Clean HTML (unwrap disallowed tags, keep allowed tags only)
        """
        pass
    

    def scrape_platypus_article(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title_tag = soup.find('h1')  # generic title
        title = title_tag.get_text(strip=True) if title_tag else "Untitled"
        
        # find main content by structure, e.g., article div
        content_div = soup.find('div', class_='dc-page-seo-wrapper')
        if not content_div:
            content_div = soup  # fallback to whole page
        
        # collect allowed tags and unwrap everything else
        allowed_tags = {'a', 'b', 'i', 'em', 'strong', 'u', 's', 'blockquote',
                        'code', 'pre', 'p', 'ul', 'ol', 'li', 'br', 'hr', 'img'}
        
        for tag in content_div.find_all():
            if tag.name not in allowed_tags:
                tag.unwrap()
        
        # Join children HTML for Telegraph
        html_content = ''.join(str(child) for child in content_div.contents)
        
        return title, html_content



from bs4 import BeautifulSoup
from telegraph import Telegraph
import requests
import json
import os

ARTICLE_URL = 'https://platypus1917.org/2025/02/01/forward-looking-return-an-interview-with-disco-elysium-writer-helen-hindpere/'
TOKEN_FILE = 'graph_bot.json'

# --- Setup Telegraph ---

if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        account_data = json.load(f)
        telegraph = Telegraph(access_token=account_data['access_token'])
else:
    account_data = telegraph.create_account(
        short_name='konstantinopolka',
        author_name='Platypus Review',
        author_url='https://platypus1917.org/platypus-review/'
    )
    with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(account_data, f, ensure_ascii=False, indent=4)

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
