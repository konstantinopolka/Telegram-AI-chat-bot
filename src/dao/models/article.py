#third party libraries
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, Text, JSON, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

#local 
from src.dao.database_instance import Base
from src.dao.models.review import Review

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    original_url = Column(String(500), nullable=False)

    # Foreign key to reviews.id
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False)

    telegraph_urls = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc), onupdate=lambda: datetime.now(tz=timezone.utc))
    authors = Column(JSON, default=list)
    
    # Relationship: many articles -> one review
    review = relationship("Review", back_populates="articles")
    
    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}', review_id={self.review_id})>"
