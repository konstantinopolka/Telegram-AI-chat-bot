from telegraph import Telegraph
import json
import os

class TelegraphManager:
    
    def __init__(self, access_token: str):
        TOKEN_FILE = 'graph_bot.json'
        telegraph = None
        self.__setup_telegraph()
        
        
    def __setup_telegraph(self):
        # --- Setup Telegraph ---
        telegraph = Telegraph()

        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'r', encoding='utf-8') as f:
                account_data = json.load(f)
                telegraph = Telegraph(access_token=account_data['access_token'])
        else:
            account_data = telegraph.create_account(
                short_name='konstantinopolka',
                author_name='Platypus Review',
                author_url='https://platypus1917.org/platypus-review/'
            )
            with open(self.TOKEN_FILE, 'w', encoding='utf-8') as f:
                json.dump(account_data, f, ensure_ascii=False, indent=4)


    async def create_article(self, article):
        """
        Create one or more Telegraph articles if the content exceeds limits.
        Returns list of Telegraph URLs.
        """
        chunks = self.split_content(article)
        # --- Create Telegraph pages ---
        telegraph_urls = []
        for i, chunk in enumerate(chunks):
            print(i)
            print(chunk)
            print(len(chunk))
            page = self.telegraph.create_page(
                title=title if i == 0 else f"{title} (part {i+1})",
                html_content=chunk,
                author_name="Platypus Review"
            )
            telegraph_urls.append(page['url'])

        print("Created Telegraph articles:")
        print("\n".join(telegraph_urls))
        
    def split_content(self, content_div):
        # --- Split content safely into chunks ---
        # TO-DO: update content_div
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
        return chunks

