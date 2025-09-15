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
        # TO-DO: only if the article is longer than 60kb: add links to previous page and to the next page if there any
        # TO-DO: only if the article is longer than 60kb: if you have to divide the article, then in equal chunks
    
        # TO-DO: add data of the creation of the article to <p class="has-text-align-right"><a href="https://platypus1917.org/category/pr/issue-179/"><em>Platypus Review</em> 179</a> | September 2025</p>
        

        title = article.title
        content = self._add_reposting_date(article.content)  # Modify content first
        chunks = self.split_content(content, title)
        
        # --- Create Telegraph pages ---
        telegraph_urls = []
        for i, chunk in enumerate(chunks):
            chunk_title = title if i == 0 else f"{title} (part {i+1})"
            
            try:
                print(f"   📤 Creating Telegraph page {i+1}/{len(chunks)}: {chunk_title}")
                print(f"      Content: {len(chunk)} chars, {len(chunk.encode('utf-8'))} bytes")
                
                page = self.telegraph.create_page(
                    title=chunk_title,
                    html_content=chunk,
                    author_name=self.author_name
                )
                telegraph_urls.append(page['url'])
                print(f"      ✅ Created: {page['url']}")
                
            except Exception as e:
                print(f"      ❌ Telegraph API error: {str(e)}")
                # If we get a content too large error, try with smaller chunks
                if "content too large" in str(e).lower() or "too long" in str(e).lower():
                    print(f"      🔄 Content still too large, need smaller chunks")
                    # Could implement recursive splitting here
                raise e

        print(f"📄 Created {len(telegraph_urls)} Telegraph article(s)")
        return telegraph_urls
        
        
        

    def _add_reposting_date(self, content: str) -> str:
        """Find existing publication info and add repost date to it."""
        from bs4 import BeautifulSoup
        from datetime import datetime
        
        # Parse the content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Get current date for reposting
        current_date = datetime.now()
        repost_date = current_date.strftime("%Y-%m-%d")
        
        # Look for the publication info paragraph
        # Find p tag with class "has-text-align-right" containing "Platypus Review"
        pub_paragraph = soup.find('p', class_='has-text-align-right')
        
        if pub_paragraph and 'Platypus Review' in pub_paragraph.get_text():
            # Add repost date to the existing paragraph
            repost_text = f' <em>(Reposted on: {repost_date})</em>'
            pub_paragraph.append(BeautifulSoup(repost_text, 'html.parser'))
        else:
            # If no existing publication info found, create a new one with repost date
            month_year = current_date.strftime("%B %Y")
            issue_number = "179"  # Update this logic as needed
            
            pub_info_html = f'''<p class="has-text-align-right"><a href="https://platypus1917.org/category/pr/issue-{issue_number}/"><em>Platypus Review</em> {issue_number}</a> | {month_year} <em>Reposted on: {repost_date}</em></p>'''
            
            pub_info_soup = BeautifulSoup(pub_info_html, 'html.parser')
            
            # Insert at the beginning
            first_element = soup.find()
            if first_element:
                first_element.insert_before(pub_info_soup.p)
            else:
                # If no elements found, just add it as the first content
                soup.append(pub_info_soup.p)
        
        return str(soup)


    def split_content(self, content: str, title: str = ""):
        """Split HTML content string safely into chunks that fit Telegraph's limits."""
        from bs4 import BeautifulSoup
        
        # Parse the content string into BeautifulSoup
        content_soup = BeautifulSoup(content, 'html.parser')
        
        # Telegraph has a 64KB limit, but we need to account for:
        # - Title length
        # - Author metadata overhead (~100 bytes)
        # - HTML tag overhead
        # - UTF-8 encoding (some chars = multiple bytes)
        # - Telegraph internal formatting overhead
        
        # Conservative limit: Reserve space for title and overhead
        title_bytes = len(title.encode('utf-8'))
        overhead_bytes = 2000  # Conservative overhead estimate
        MAX_CONTENT_BYTES = 65536 - title_bytes - overhead_bytes  # ~63KB for content
        
        # Convert to character limit (assume average 1.1 bytes per char for safety)
        MAX_CHARS = int(MAX_CONTENT_BYTES / 1.1) 
        
        print(f"   📏 Split limits: Title={title_bytes}B, Max content={MAX_CHARS} chars")
        
        blocks = content_soup.find_all(['p', 'ul', 'ol', 'blockquote', 'pre', 'img', 'hr'])
        
        chunks = []
        current_chunk = ""

        for block in blocks:
            block_html = str(block)
            block_bytes = len(block_html.encode('utf-8'))
            current_bytes = len(current_chunk.encode('utf-8'))
            
            # Check both character and byte limits
            if (current_bytes + block_bytes > MAX_CONTENT_BYTES or 
                len(current_chunk) + len(block_html) > MAX_CHARS):
                
                if current_chunk:  # Don't add empty chunks
                    chunks.append(current_chunk)
                    print(f"   📄 Chunk {len(chunks)}: {len(current_chunk)} chars, {len(current_chunk.encode('utf-8'))} bytes")
                current_chunk = block_html
            else:
                current_chunk += block_html

        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk)
            print(f"   📄 Chunk {len(chunks)}: {len(current_chunk)} chars, {len(current_chunk.encode('utf-8'))} bytes")
            
        print(f"   ✂️  Split into {len(chunks)} chunk(s)")
        return chunks

