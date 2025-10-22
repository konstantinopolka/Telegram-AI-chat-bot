#default libraries
from typing import Optional, List

#third party libraries
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

#local 
# from src.dao.models import Article

class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    id: Optional[int] = Field(default=None, primary_key=True)
    source_url: str = Field(max_length=500)
    created_at: date
    # Relationship: one review -> many articles
    articles: Optional[List["Article"]] = Relationship(back_populates="review")
    

