import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Define naming convention for constraints
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

Base = declarative_base(metadata=MetaData(naming_convention=naming_convention))

import src.dao.models 

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")
engine = create_engine(DATABASE_URL, echo=True)


AsyncSessionLocal = None
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL", "sqlite+aiosqlite:///dev.db")
if ASYNC_DATABASE_URL:
    async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    
# Base.metadata.create_all(engine)


