#standard libraries
import json
import os
from typing import List



#third party libraries
from telegraph import Telegraph

#local 
from src.dao.models import Article
from src.scraping.constants import ALLOWED_TAGS

class TelegraphManager:
    
    def __init__(self, access_token: str = None):
        self.TOKEN_FILE = 'graph_bot.json'  # Keep for backward compatibility
        self.telegraph = None
        # Use provided token or get from environment
        self.access_token = access_token or os.getenv('TELEGRAPH_ACCESS_TOKEN')
        self.short_name = os.getenv('TELEGRAPH_SHORT_NAME', 'konstantinopolka')
        self.author_name = os.getenv('TELEGRAPH_AUTHOR_NAME', 'Platypus Review')
        self.author_url = os.getenv('TELEGRAPH_AUTHOR_URL', 'https://platypus1917.org/platypus-review/')
        self.__setup_telegraph()
        
        
    def __setup_telegraph(self):
        # --- Setup Telegraph ---
        self.telegraph = Telegraph()

        # First try to use environment variables
        if self.access_token and self.access_token != "test_token":
            self.telegraph = Telegraph(access_token=self.access_token)
        # Fallback to JSON file for backward compatibility
        elif os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'r', encoding='utf-8') as f:
                account_data = json.load(f)
                self.telegraph = Telegraph(access_token=account_data['access_token'])
        else:
            # Create new account if no credentials available
            account_data = self.telegraph.create_account(
                short_name=self.short_name,
                author_name=self.author_name,
                author_url=self.author_url
            )
            # Save to JSON file as backup (optional)
            with open(self.TOKEN_FILE, 'w', encoding='utf-8') as f:
                json.dump(account_data, f, ensure_ascii=False, indent=4)


    async def create_article(self, article: Article) -> List[str]:
        """
        Create one or more Telegraph articles if the content exceeds limits.
        Returns list of Telegraph URLs.
        """
        title = article.title
        
        chunks = self.split_content(article.content)
        # --- Create Telegraph pages ---
        telegraph_urls = []
        for i, chunk in enumerate(chunks):
            print(i)
            print(chunk)
            print(len(chunk))
            page = self.telegraph.create_page(
                title=title if i == 0 else f"{title} (part {i+1})",
                html_content=chunk,
                author_name=self.author_name
            )
            telegraph_urls.append(page['url'])

        print("Created Telegraph articles:")
        print("\n".join(telegraph_urls))
        return telegraph_urls
        
    def split_content(self, content: str):
        """Split HTML content string safely into chunks."""
        from bs4 import BeautifulSoup
        
        # Parse the content string into BeautifulSoup
        content_soup = BeautifulSoup(content, 'html.parser')
        
        # --- Split content safely into chunks ---
        MAX_CHARS = 60000
        blocks = content_soup.find_all(['p', 'ul', 'ol', 'blockquote', 'pre', 'img', 'hr'])
        
        # 1. add auth
        
        # HTML tags allowed in cleaned content for Telegraph compatibility
        ALLOWED_TAGS = {
            'a', 'b', 'i', 'em', 'strong', 'u', 's', 'blockquote',
            'code', 'pre', 'p', 'ul', 'ol', 'li', 'br', 'hr', 'img'
        }
                
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
        return chunks

