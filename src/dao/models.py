import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()


class User(Base):
    __tablename__ = "reposting_bot_users"
    
    telegram_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    is_admin = Column(Boolean, default=True)
    registered_at = Column(DateTime, default=lambda: datetime.now(tz=timezone.utc))
    
    def __repr__(self):
        return f"<User(id={self.telegram_id}, username={self.username})>"
    
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")
    
engine = create_engine(DATABASE_URL, echo=True)
# Base.metadata.create_all(engine)


