from typing import Dict, Any, List
from src.dao.models.article import Article
from src.logging_config import get_logger

logger = get_logger(__name__)

class ArticleFactory:
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Prevent re-initialization
        if self._initialized:
            return
        
        self._initialized = True
        
    
    @staticmethod
    def from_scraper_data(raw_review_data: Dict[str, Any]) -> List[Article]:
        """
        Create Article instances from raw scraped data.
        
        Args:
            raw_review_data: Dict containing 'articles' list and 'review_id'
            
        Returns:
            List of validated Article instances
        """
        articles = []
        review_id = raw_review_data.get('review_id')
        
        for article_dict in raw_review_data.get('articles', []):
            try:
                # Add review_id to each article if not already present
                if 'review_id' not in article_dict:
                    article_dict['review_id'] = review_id
                    
                article = Article(**article_dict)
                articles.append(article)
                logger.debug(f"Created article: {article.title[:50]}...")
            except Exception as e:
                logger.error(f"Failed to create article schema: {e}", exc_info=True)
                continue
        
        logger.info(f"Created {len(articles)} articles from scraper data")        
        return articles
    
    
article_factory = ArticleFactory()