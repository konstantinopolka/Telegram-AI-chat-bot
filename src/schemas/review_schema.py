from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from src.schemas import ArticleSchema


class ReviewSchema(BaseModel):
    
    id: int
    source_url: str
    created_at: Optional[datetime]
    
    # Relationship: one review -> many articles
    articles: List[ArticleSchema] = []
    
    class Config:
        orm_mode = True



