import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
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
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL", "sqlite+aiosqlite:///dev.db")
    
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
engine = create_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(async_engine, class_ = AsyncSession, expire_on_commit=False)
# Base.metadata.create_all(engine)


