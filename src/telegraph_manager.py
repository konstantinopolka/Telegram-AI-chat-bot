from telegraph import Telegraph
import json
import os

class TelegraphManager:
    
    def __init__(self, access_token: str):
        TOKEN_FILE = 'graph_bot.json'
        telegraph = Telegraph()
        self.access_token = access_token
        
    def __setup_telegraph(self):
        # --- Setup Telegraph ---

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
        pass
