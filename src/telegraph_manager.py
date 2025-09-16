#standard libraries
import json
import os
from typing import List
from bs4 import BeautifulSoup


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
        content = article.content
        content = self._add_reposting_date(article.content)  # Modify content first
        
        # Check if article will be split into multiple parts
        # We need to know this beforehand to reserve space for navigation links
        estimated_chunks = self._estimate_chunks_count(content, title)
        will_be_multipart = estimated_chunks > 1
        
        chunks = self.split_content(content, title, reserve_space_for_nav=will_be_multipart)
        
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

        # If multi-part article, add navigation links
        if len(telegraph_urls) > 1:
            print(f"   🔗 Adding navigation links to {len(telegraph_urls)} parts...")
            await self._add_navigation_links(telegraph_urls, chunks, title)

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
        reposting_date = current_date.strftime("%Y-%m-%d")
        
        # Look for the publication info paragraph
        # Find p tag with class "has-text-align-right" containing "Platypus Review"
        pub_paragraph = soup.find('p', class_='has-text-align-right')
        
        if pub_paragraph and 'Platypus Review' in pub_paragraph.get_text():
            # Add repost date to the existing paragraph
            repost_text = f' <em>(Reposted on: {reposting_date})</em>'
            pub_paragraph.append(BeautifulSoup(repost_text, 'html.parser'))
        else:
            # If no existing publication info found, create a new one with repost date
            month_year = current_date.strftime("%B %Y")
            issue_number = "179"  # Update this logic as needed
            
            pub_info_html = f'''<p class="has-text-align-right"><a href="https://platypus1917.org/category/pr/issue-{issue_number}/"><em>Platypus Review</em> {issue_number}</a> | {month_year} <em>Reposted on: {reposting_date}</em></p>'''
            
            pub_info_soup = BeautifulSoup(pub_info_html, 'html.parser')
            
            # Insert at the beginning
            first_element = soup.find()
            if first_element:
                first_element.insert_before(pub_info_soup.p)
            else:
                # If no elements found, just add it as the first content
                soup.append(pub_info_soup.p)
        
        return str(soup)

    def _estimate_chunks_count(self, content: str, title: str) -> int:
        """Estimate how many chunks the content will be split into."""
        # Use a quick estimation without actually processing all blocks
        content_bytes = len(content.encode('utf-8'))
        title_bytes = len(title.encode('utf-8'))
        overhead_bytes = 2000
        max_content_bytes = 65536 - title_bytes - overhead_bytes
        
        estimated_chunks = max(1, (content_bytes + max_content_bytes - 1) // max_content_bytes)
        return estimated_chunks

    async def _add_navigation_links(self, telegraph_urls: List[str], original_chunks: List[str], title: str):
        """Add navigation links to multi-part Telegraph articles."""
        for i, url in enumerate(telegraph_urls):
            # Get the page path from URL for editing
            page_path = url.split('/')[-1]
            
            # Create navigation links
            nav_links = self._create_navigation_links(i, len(telegraph_urls), telegraph_urls, title)
            
            # Add navigation to the existing content
            updated_content = self._add_nav_to_content(original_chunks[i], nav_links, i == 0)
            
            try:
                # Update the Telegraph page with navigation links
                self.telegraph.edit_page(
                    path=page_path,
                    title=title if i == 0 else f"{title} (part {i+1})",
                    html_content=updated_content,
                    author_name=self.author_name
                )
                print(f"      🔗 Added navigation to part {i+1}")
                
            except Exception as e:
                print(f"      ❌ Failed to add navigation to part {i+1}: {str(e)}")

    def _create_navigation_links(self, current_index: int, total_parts: int, urls: List[str], title: str) -> dict:
        """Create navigation link HTML for current part."""
        nav = {
            'top': '',
            'bottom': ''
        }
        
        links = []
        
        # Previous part link
        if current_index > 0:
            prev_url = urls[current_index - 1]
            prev_title = title if current_index == 1 else f"{title} (part {current_index})"
            links.append(f'<br><a href="{prev_url}">← Previous: {prev_title}</a>')
        
        # Next part link
        if current_index < total_parts - 1:
            next_url = urls[current_index + 1]
            next_title = f"{title} (part {current_index + 2})"
            links.append(f'<br><a href="{next_url}">Next: {next_title} →</a>')
        
        if links:
            # Create navigation HTML
            nav_html = f'<p><strong>Navigation:</strong> {"  ".join(links)}</p><hr>'
            nav['top'] = nav_html
            nav['bottom'] = f'<hr>{nav_html}'
        
        return nav

    def _add_nav_to_content(self, content: str, nav_links: dict, is_first_part: bool) -> str:
        """Add navigation links to content at the beginning and end."""
        if not nav_links['top']:
            return content
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Add navigation at the top (after reposting date if it's the first part)
        top_nav_soup = BeautifulSoup(nav_links['top'], 'html.parser')
        
        if is_first_part:
            # Find the reposting date paragraph and insert after it
            pub_paragraph = soup.find('p', class_='has-text-align-right')
            if pub_paragraph:
                # Insert after the publication info
                for element in reversed(top_nav_soup.contents):
                    if hasattr(element, 'name'):
                        pub_paragraph.insert_after(element)
            else:
                # Insert at the very beginning
                first_element = soup.find()
                if first_element:
                    for element in reversed(top_nav_soup.contents):
                        if hasattr(element, 'name'):
                            first_element.insert_before(element)
        else:
            # For subsequent parts, add at the very beginning
            first_element = soup.find()
            if first_element:
                for element in reversed(top_nav_soup.contents):
                    if hasattr(element, 'name'):
                        first_element.insert_before(element)
        
        # Add navigation at the bottom
        bottom_nav_soup = BeautifulSoup(nav_links['bottom'], 'html.parser')
        # Add all elements from bottom navigation
        for element in bottom_nav_soup.find_all():
            soup.append(element)
        
        return str(soup)


    def split_content(self, content: str, title: str = "", reserve_space_for_nav: bool = False) -> List[str]:
        """Split HTML content string safely into chunks that fit Telegraph's limits."""
        from bs4 import BeautifulSoup
        
        def _get_blocks(content_soup: BeautifulSoup) -> List[BeautifulSoup]: 
                
            # Get all top-level elements that could be meaningful chunks
            # This includes block-level elements and standalone inline elements
            blocks = []
            
            
            # First, get traditional block-level elements
            block_elements = content_soup.find_all(['p', 'ul', 'ol', 'blockquote', 'pre', 'hr'])
            blocks.extend(block_elements)
            
            # Then handle standalone img tags (they might not be in paragraphs)
            standalone_imgs = content_soup.find_all('img')
            for img in standalone_imgs:
                # Only add if it's not already inside a block element we found
                if not any(img in block.find_all('img') if hasattr(block, 'find_all') else False for block in block_elements):
                    blocks.append(img)
            
            # Handle any remaining text or inline elements that aren't wrapped in blocks
            for element in content_soup.children:
                if hasattr(element, 'name') and element.name in ALLOWED_TAGS:
                    # Check if this element is inline and not already captured
                    if element.name in ['a', 'b', 'i', 'em', 'strong', 'u', 's', 'code', 'br']:
                        # Only add if it's not already inside a block we found
                        if not any(element in block.descendants if hasattr(block, 'descendants') else False for block in blocks):
                            blocks.append(element)
                elif hasattr(element, 'string') and element.string and element.string.strip():  # Text nodes
                    # Wrap standalone text in a paragraph for proper handling
                    text_content = element.string.strip()
                    if text_content and not any(text_content in str(block) for block in blocks):
                        # Create a temporary paragraph wrapper for text
                        temp_p = content_soup.new_tag('p')
                        temp_p.string = text_content
                        blocks.append(temp_p)
            
            # Sort blocks by their position in the original document
            def get_position(element):
                try:
                    return list(content_soup.descendants).index(element)
                except ValueError:
                    return 999999  # Put new elements at the end
            
            blocks.sort(key=get_position)
            return blocks
        
        
        def _get_chunks(blocks, title: str) -> List[str]:
            # Conservative limit: Reserve space for title and overhead
            title_bytes = len(title.encode('utf-8'))
            overhead_bytes = 2000  # Conservative overhead estimate
            
            # Reserve additional space for navigation links if needed
            nav_overhead = 0
            if reserve_space_for_nav:
                # Estimate space needed for navigation links
                # Example: "Navigation: ← Previous: Title | Next: Title (part 2) →" + HR tags
                estimated_nav_size = len(title.encode('utf-8')) * 2 + 200  # Conservative estimate
                nav_overhead = estimated_nav_size * 2  # Top and bottom navigation
                
            MAX_CONTENT_BYTES = 64000 - title_bytes - overhead_bytes - nav_overhead  # More conservative limit
            
            # Convert to character limit (assume average 1.2 bytes per char for safety with UTF-8)
            MAX_CHARS = int(MAX_CONTENT_BYTES / 1.2) 
            
            reserved_info = f", Nav reserved: {nav_overhead}B" if reserve_space_for_nav else ""
            print(f"   📏 Split limits: Title={title_bytes}B, Max content={MAX_CHARS} chars{reserved_info}")
            
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

        
        content_soup = BeautifulSoup(content, 'html.parser')
        blocks = _get_blocks(content_soup)
        chunks = _get_chunks(blocks, title)
        return chunks



