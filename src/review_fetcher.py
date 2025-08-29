from typing import List



class ReviewFetcher:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def fetch_review(self, review_url: str) -> List[str]:
        """
        Fetch the HTML of the review page and extract article URLs.
        Returns a list of article URLs.
        """
        pass

    async def fetch_article(self, article_url: str) -> List[str]:
        """
        Fetch a single article and parse title and content.
        Returns an Article object.
        """
        pass

    async def parse_article_html(self, html: str) -> str:
        """
        Clean HTML (unwrap disallowed tags, keep allowed tags only)
        """
        pass
