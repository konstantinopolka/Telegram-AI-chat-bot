#default libraries
from typing import Optional, List

#third party libraries
from datetime import date
from sqlmodel import SQLModel, Field, Relationship, JSON


#local 
# from src.dao.models.review import Review

class Article(SQLModel, table=True):
    __tablename__ = "articles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    content: str 
    original_url: str = Field(max_length=500)

        # Foreign key to reviews.id
    review_id: int = Field(foreign_key="reviews.id")
    telegraph_urls: Optional[List[str]] = Field(default_factory=list, sa_type=JSON)
    publication_date: date
    authors: Optional[List[str]] = Field(default_factory=list, sa_type=JSON)
    
    # Relationship: many articles -> one review
    review: Optional["Review"] = Relationship(back_populates="articles")