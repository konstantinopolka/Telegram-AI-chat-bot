from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, Text, JSON
from datetime import datetime, timezone
from typing import List
from src.dao.database_instance import Base


class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    original_url = Column(String(500), nullable=False)
    review_id = Column(Integer, nullable=False)
    telegraph_urls = Column(JSON, default=list)  # URLs after publishing
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc), onupdate=lambda: datetime.now(tz=timezone.utc))
    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}', review_id={self.review_id})>"


