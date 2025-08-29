from sqlalchemy import Column, String, Boolean, DateTime, BigInteger
from datetime import datetime, timezone
from src.dao.database_instance import Base

class User(Base):
    __tablename__ = "reposting_bot_users"
    
    telegram_id = Column(BigInteger, primary_key=True)
    username = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=True)
    phone = Column(String(20), nullable=True)
    is_admin = Column(Boolean, default=True)
    registered_at = Column(DateTime(timezone=True), default=lambda: datetime.now(tz=timezone.utc))
    
    def __repr__(self):
        return f"<User(id={self.telegram_id}, username={self.username})>"
    