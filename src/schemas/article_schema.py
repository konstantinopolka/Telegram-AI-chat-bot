from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ArticleSchema(BaseModel):
    id: Optional[int] = None  # Will be set when saved to DB
    title: str
    content: str
    original_url: str
    review_id: Optional[int] = None  # Will be set during processing
    telegraph_urls: List[str] = []
    authors: List[str] = []
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True