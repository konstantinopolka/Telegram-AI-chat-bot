from typing import Generic, TypeVar, Optional, List, Type
from sqlmodel import SQLModel, select
from sqlalchemy import func

from src.dao.core.database_manager import db_manager
from src.logging_config import get_logger

logger = get_logger(__name__)

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    """
    Abstract base repository with common CRUD operations.
    
    All repositories should inherit from this class.
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Args:
            model: SQLModel class (e.g., User, Article, Review)
        """
        self.model = model
        self.db = db_manager
        logger.debug(f"Initialized {self.__class__.__name__} for model: {model.__name__}")
    
    async def save(self, obj: ModelType) -> ModelType:
        """
        Create a new record.
        
        Args:
            obj: Model instance to create
            
        Returns:
            Created model instance with ID populated
        """
        logger.debug(f"Creating new {self.model.__name__} record")
        try:
            async with self.db.get_async_session() as session:
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                logger.info(f"Created {self.model.__name__} with ID: {getattr(obj, 'id', 'N/A')}")
                return obj
        except Exception as e:
            logger.error(f"Failed to create {self.model.__name__}: {e}", exc_info=True)
            raise
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get record by ID.
        
        Args:
            id: Primary key value
            
        Returns:
            Model instance or None if not found
        """
        logger.debug(f"Fetching {self.model.__name__} by ID: {id}")
        try:
            async with self.db.get_async_session() as session:
                result = await session.get(self.model, id)
                if result:
                    logger.debug(f"Found {self.model.__name__} with ID: {id}")
                else:
                    logger.debug(f"{self.model.__name__} with ID {id} not found")
                return result
        except Exception as e:
            logger.error(f"Failed to fetch {self.model.__name__} by ID {id}: {e}", exc_info=True)
            raise
    
    async def get_all(self) -> List[ModelType]:
        """
        Get all records.
        
        Returns:
            List of all model instances
        """
        logger.debug(f"Fetching all {self.model.__name__} records")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(select(self.model))
                records = result.scalars().all()
                logger.debug(f"Retrieved {len(records)} {self.model.__name__} records")
                return records
        except Exception as e:
            logger.error(f"Failed to fetch all {self.model.__name__} records: {e}", exc_info=True)
            raise
    
    async def update(self, obj: ModelType) -> ModelType:
        """
        Update existing record.
        
        Args:
            obj: Model instance with updated values
            
        Returns:
            Updated model instance
        """
        obj_id = getattr(obj, 'id', 'N/A')
        logger.debug(f"Updating {self.model.__name__} with ID: {obj_id}")
        try:
            async with self.db.get_async_session() as session:
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                logger.info(f"Updated {self.model.__name__} with ID: {obj_id}")
                return obj
        except Exception as e:
            logger.error(f"Failed to update {self.model.__name__} with ID {obj_id}: {e}", exc_info=True)
            raise
    
    async def delete(self, id: int) -> bool:
        """
        Delete record by ID.
        
        Args:
            id: Primary key value
            
        Returns:
            True if deleted, False if not found
        """
        logger.debug(f"Attempting to delete {self.model.__name__} with ID: {id}")
        try:
            async with self.db.get_async_session() as session:
                obj = await session.get(self.model, id)
                if obj:
                    await session.delete(obj)
                    await session.commit()
                    logger.info(f"Deleted {self.model.__name__} with ID: {id}")
                    return True
                logger.debug(f"{self.model.__name__} with ID {id} not found for deletion")
                return False
        except Exception as e:
            logger.error(f"Failed to delete {self.model.__name__} with ID {id}: {e}", exc_info=True)
            raise
    
    async def exists(self, id: int) -> bool:
        """
        Check if record exists.
        
        Args:
            id: Primary key value
            
        Returns:
            True if exists, False otherwise
        """
        logger.debug(f"Checking if {self.model.__name__} exists with ID: {id}")
        obj = await self.get_by_id(id)
        exists = obj is not None
        logger.debug(f"{self.model.__name__} with ID {id} exists: {exists}")
        return exists
    
    async def count(self) -> int:
        """
        Count total records.
        
        Returns:
            Total number of records
        """
        logger.debug(f"Counting total {self.model.__name__} records")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(self.model).with_only_columns(func.count())
                )
                count = result.scalar()
                logger.debug(f"Total {self.model.__name__} count: {count}")
                return count
        except Exception as e:
            logger.error(f"Failed to count {self.model.__name__} records: {e}", exc_info=True)
            raise