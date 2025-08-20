
from sqlalchemy import Column, Integer, String, Boolean, Datetime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "reposting_bot_users"
    
    telegram_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    is_admin = Column(Boolean, default=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(id={self.telegram_id}, username={self.username})>"