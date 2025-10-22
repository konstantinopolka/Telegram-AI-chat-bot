from typing import List
from src.logging_config import get_logger
from src.dao.models import Article, Review

logger = get_logger(__name__)


class ChannelPoster:
    def __init__(self, bot_instance, channel_id: int):
        self.bot = bot_instance
        self.channel_id = channel_id

    async def post_telegraph_urls(self, telegraph_urls: List[str]):
        """
        Post one or multiple Telegraph URLs to the channel.
        
        Args:
            telegraph_urls: List of Telegraph article URLs to post
        """
        pass
    
    async def post_article(self, article: Article):
        """
        Post an Article's Telegraph URLs to the channel.
        
        Args:
            article: Article instance with telegraph_urls populated
        """
        pass
    
    async def post_review(self, review: Review):
        """
        Post all articles from a Review to the channel.
        
        Args:
            review: Review instance with articles populated
        """
        pass
            