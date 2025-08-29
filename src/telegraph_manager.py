class TelegraphManager:
    def __init__(self, access_token: str):
        self.access_token = access_token

    async def create_article(self, article):
        """
        Create one or more Telegraph articles if the content exceeds limits.
        Returns list of Telegraph URLs.
        """
        pass
