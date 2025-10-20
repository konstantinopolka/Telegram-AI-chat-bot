from typing import List
from src.logging_config import get_logger
from src.dao.models import Article, Review

logger = get_logger(__name__)


class ChannelPoster:
    def __init__(self, bot_instance, channel_id: int):
        self.bot = bot_instance
        self.channel_id = channel_id

    async def post_article(self, telegraph_urls: List[str]):
        """
        Post one or multiple Telegraph URLs to the channel
        """
        pass
    
    async def post_article(self, article: Article):
        """
        Post one or multiple Telegraph URLs to the channel
        """
        pass
    
    async def post_review(self, review: Review )
            