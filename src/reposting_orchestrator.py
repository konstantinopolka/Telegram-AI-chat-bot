from src.archive_scanner import ArchiveScanner
from src.review_orchestrator import ReviewOrchestrator
from src.dao.models import Review
from typing import Set, Tuple
from src.bot_orchestrator import BotOrchestrator


class RepostingOrchestrator:
    
    """
    Workflow:
    
    
    """
    
    def __init__(self):
        self.archive_scanner: ArchiveScanner = ArchiveScanner()
        self.bot_orchestrator: BotOrchestrator = BotOrchestrator()
        self.review_orchestrator: ReviewOrchestrator = None
        
        
    
    async def scan_and_process_new_reviews(self, post_recent: bool = True):
        new_reviews_urls:  Set[str] = await self.archive_scanner.get_new_reviews()
        for review_url in new_reviews_urls:
            self.review_orchestrator: ReviewOrchestrator = ReviewOrchestrator(review_url)
            result: Tuple[Review, bool] = await self.review_orchestrator.process_review_batch()
            review, was_created = result
            if was_created:
                # TO-DO: Handle reposting in telegram
                pass
    
    
    async def start_telegram_bot(self): 
        self.bot_orchestrator.start()
    
    