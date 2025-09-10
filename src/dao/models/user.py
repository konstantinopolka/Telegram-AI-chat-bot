    #default libraries
from typing import Optional, List

#third party libraries
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    __tablename__ = "reposting_bot_users"
    
    telegram_id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=50)
    first_name: str = Field(max_length=50)
    last_name: Optional[str] = Field(max_length=50)
    phone: Optional[str] = Field(max_length=20)
    is_admin: bool = Field(default=True)
    registered_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    