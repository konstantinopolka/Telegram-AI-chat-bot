class RepostingOrchestrator:
    def __init__(self, review_fetcher, telegraph_manager, db_session, bot_handler, channel_poster):
        self.fetcher = review_fetcher
        self.telegraph = telegraph_manager
        self.db = db_session
        self.bot = bot_handler
        self.channel = channel_poster

    async def process_review(self, review_url: str):
        """
        Full workflow:
        - fetch articles from review
        - create Telegraph articles
        - save metadata to DB
        - post to channel
        """
        pass
