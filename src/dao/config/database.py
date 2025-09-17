import os
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlmodel import SQLModel

load_dotenv()

# Database URLs
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL", "sqlite+aiosqlite:///dev.db")

# Naming convention for constraints
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s", 
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Set up metadata BEFORE importing models
SQLModel.metadata = MetaData(naming_convention=naming_convention)

# Import models to register them with metadata
import src.dao.models