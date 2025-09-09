from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ArticleSchema(BaseModel):
    id: int
    title: str
    content: str
    original_url: str
    review_id: int
    telegraph_urls: List[str] = []
    authors: List[str] = []
    created_at: Optional[datetime]

    class Config:
        orm_mode = True