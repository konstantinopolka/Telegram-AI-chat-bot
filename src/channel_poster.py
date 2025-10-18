from typing import List
from src.logging_config import get_logger

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
            