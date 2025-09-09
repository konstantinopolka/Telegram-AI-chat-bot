from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from src.dao.database_instance import Base
from sqlalchemy.orm import relationship


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True)
    source_url = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc))
    
    # Relationship: one review -> many articles
    articles = relationship("Article", back_populates="review")
    
    
    def __repr__(self):
        return f"<Review(id={self.id}, title='{self.title}')>"

