import os
from typing import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import SQLModel
from dotenv import load_dotenv
from src.logging_config import get_logger

logger = get_logger(__name__)

# Define naming convention BEFORE imports
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

SQLModel.metadata = MetaData(naming_convention=naming_convention)

# Import models AFTER metadata setup
import src.dao.models


class DatabaseManager:
    """
    Singleton Database Manager with both sync and async engines.
    
    Usage:
        # Get instance
        db = DatabaseManager()
        
        # Use async session
        async with db.get_async_session() as session:
            # your async operations
            pass
        
        # Use sync session (for Alembic migrations)
        with db.get_sync_session() as session:
            # your sync operations
            pass
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Prevent re-initialization
        if self._initialized:
            return
            
        load_dotenv()
        
        # Sync engine (for migrations, admin tasks)
        self.sync_database_url = os.getenv("DATABASE_URL", "sqlite:///dev.db")
        self.sync_engine = create_engine(
            self.sync_database_url,
            echo=os.getenv("DB_ECHO", "false").lower() == "true",
            pool_pre_ping=True,  # Verify connections before using
        )
        
        # Async engine (for bot operations)
        self.async_database_url = os.getenv(
            "ASYNC_DATABASE_URL",
            "sqlite+aiosqlite:///dev.db"
        )
        self.async_engine = create_async_engine(
            self.async_database_url,
            echo=os.getenv("DB_ECHO", "false").lower() == "true",
            pool_pre_ping=True,
        )
        
        # Session factories
        self.SyncSessionLocal = sessionmaker(
            bind=self.sync_engine,
            class_=Session,
            expire_on_commit=False,
        )
        
        self.AsyncSessionLocal = async_sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        self._initialized = True
        logger.info("=" * 60)
        logger.info("DatabaseManager initialized successfully")
        logger.info(f"Sync Database URL: {self.sync_database_url}")
        logger.info(f"Async Database URL: {self.async_database_url}")
        logger.info(f"DB Echo: {os.getenv('DB_ECHO', 'false')}")
        logger.info("=" * 60)
    
    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get async database session (context manager).
        
        Usage:
            async with db.get_async_session() as session:
                result = await session.execute(select(User))
        """
        logger.debug("Creating async database session")
        async with self.AsyncSessionLocal() as session:
            try:
                logger.debug("Async session created, yielding to caller")
                yield session
                logger.debug("Committing async session")
                await session.commit()
                logger.debug("Async session committed successfully")
            except Exception as e:
                logger.error(f"Error in async session, rolling back: {e}", exc_info=True)
                await session.rollback()
                logger.debug("Async session rolled back")
                raise
            finally:
                logger.debug("Closing async session")
                await session.close()
    
    @contextmanager
    def get_sync_session(self) -> Generator[Session, None, None]:
        """
        Get sync database session (context manager).
        
        Usage:
            with db.get_sync_session() as session:
                result = session.execute(select(User))
        """
        logger.debug("Creating sync database session")
        session = self.SyncSessionLocal()
        try:
            logger.debug("Sync session created, yielding to caller")
            yield session
            logger.debug("Committing sync session")
            session.commit()
            logger.debug("Sync session committed successfully")
        except Exception as e:
            logger.error(f"Error in sync session, rolling back: {e}", exc_info=True)
            session.rollback()
            logger.debug("Sync session rolled back")
            raise
        finally:
            logger.debug("Closing sync session")
            session.close()
    
    async def create_all_tables(self):
        """Create all tables (use Alembic migrations instead in production)"""
        logger.warning("Creating all tables directly (use Alembic migrations in production)")
        logger.info("Starting table creation")
        async with self.async_engine.begin() as conn:
            logger.debug("Creating tables using SQLModel metadata")
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("All tables created successfully")
    
    async def drop_all_tables(self):
        """Drop all tables (DANGEROUS - use with caution)"""
        logger.critical("DANGER: Dropping all tables!")
        logger.warning("This will delete ALL data in the database")
        async with self.async_engine.begin() as conn:
            logger.debug("Dropping all tables")
            await conn.run_sync(SQLModel.metadata.drop_all)
        logger.warning("All tables dropped")
    
    async def close(self):
        """Close all connections"""
        logger.info("Closing database connections")
        logger.debug("Disposing async engine")
        await self.async_engine.dispose()
        logger.debug("Disposing sync engine")
        self.sync_engine.dispose()
        logger.info("All database connections closed")


# Singleton instance (import this in other modules)
db_manager = DatabaseManager()