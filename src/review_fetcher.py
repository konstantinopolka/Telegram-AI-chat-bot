from typing import List

import requests
from bs4 import BeautifulSoup

class ReviewFetcher:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_review(self) -> List[str]:
        articles_urls: List[str] = None
        response = requests.get(self.base_url)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        pass


    async def fetch_article(self, article_url: str) -> List[str]:
        """
        Fetch a single article and parse title and content.
        Returns an Article object.
        """
        response = requests.get(article_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
                # Find the main content container
        content_div = soup.find('div', class_='dc-page-seo-wrapper')
        if content_div:
            for para in content_div.find_all('p'):
                print(para.text.strip())
        else:
            print("No article content found.")
            
        print(content_div.prettify())
        
        #dc-page-seo-wrapper dc-layout-one-sidebar
        #dc-page-seo-wrapper dc-layout-full-width
    

    async def parse_article_html(self, html: str) -> str:
        """
        Clean HTML (unwrap disallowed tags, keep allowed tags only)
        """
        pass


fetcher = ReviewFetcher('https://platypus1917.org/2025/07/01/what-is-capitalism/')
fetcher.fetch_review()