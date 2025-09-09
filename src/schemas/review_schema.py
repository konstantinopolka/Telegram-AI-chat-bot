from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any
from src.schemas import ArticleSchema


class ReviewSchema(BaseModel):
    
    id: int
    source_url: str
    created_at: Optional[datetime]
    
    # Relationship: one review -> many articles
    articles: List[ArticleSchema] = []
    
    @classmethod
    def from_raw_data(cls, raw_data: Dict[str, Any]) -> 'ReviewSchema':
        """
        Create ReviewSchema from raw scraped data.
        
        Args:
            raw_data: Dict containing 'source_url', 'review_id', and 'articles' list
            
        Returns:
            ReviewSchema instance with validated article schemas
        """
        # Create article schemas from raw article dicts
        article_schemas = []
        for article_dict in raw_data.get('articles', []):
            try:
                article_schema = ArticleSchema(**article_dict)
                article_schemas.append(article_schema)
            except Exception as e:
                print(f"Failed to create article schema: {e}")
                continue
        
        # Create review schema
        review_data = {
            'id': raw_data.get('review_id'),
            'source_url': raw_data['source_url'],
            'articles': article_schemas,
            'created_at': raw_data.get('created_at')
        }
        
        return cls(**review_data)
    
    class Config:
        orm_mode = True



