from src.archive_scanner import ArchiveScanner
from src.review_orchestrator import ReviewOrchestrator
from src.dao.models import Review
from typing import Set, Tuple
from src.bot_handler import BotHandler

class RepostingOrchestrator:
    
    """
    Workflow:
    
    
    """
    
    def __init__(self):
        self.archive_scanner: ArchiveScanner = ArchiveScanner()
        self.bot_handler: BotHandler = BotHandler()
        
        
    
    async def scan_and_process_new_reviews(self, post_recent: bool = True):
        new_reviews_urls:  Set[str] = await self.archive_scanner.get_new_reviews()
        for review_url in new_reviews_urls:
            review_orchestrator: ReviewOrchestrator = ReviewOrchestrator(review_url)
            review, was_created: Tuple[Review, bool] = await review_orchestrator.process_review_batch()
            if was_created:
                # TO-DO: Handle reposting in telegram
                pass
    
    
    async def start_telegram_bot(self): 
        self.bot_handler.start_polling()
    