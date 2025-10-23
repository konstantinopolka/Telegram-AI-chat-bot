from typing import Generic, TypeVar, Optional, List, Type
from sqlmodel import SQLModel, select
from sqlalchemy import func
from abc import ABC, abstractmethod
from src.dao.core.database_manager import db_manager
from src.logging_config import get_logger

logger = get_logger(__name__)

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(ABC, Generic[ModelType]):
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
        Create a new record (INSERT).
        
        Args:
            obj: Model instance to create
            
        Returns:
            Created model instance with ID populated
            
        Raises:
            ValueError: If object ID already exists in database (should use update() instead)
        """
        logger.debug(f"Creating new {self.model.__name__} record")
        
        # Check if object already exists by natural key
        existing = await self.get_by(obj)
        if existing:
            # Get a meaningful identifier for the error message
            identifier = self._get_identifier_for_logging(obj, existing)
            raise ValueError(
                f"save() called on {self.model.__name__} that already exists in database "
                f"(identified by: {identifier}). Use update() instead."
            )
        
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
    
    async def update(self, obj: ModelType) -> ModelType:
        """
        Update existing record.
        The method checks if a record of the instance passed according to its constraints
        Args:
            obj: Model instance with updated values
            
        Returns:
            Updated model instance
        """
        obj_id = getattr(obj, 'id', None)
        
        if obj_id is None:
            raise ValueError(f"Cannot update {self.model.__name__} without ID. Use save() for new records.")
        
        logger.debug(f"Updating {self.model.__name__} with ID: {obj_id}")
        try:
            async with self.db.get_async_session() as session:
                existing = await session.get(self.model, obj_id)
                if not existing:
                    logger.error(f"{self.model.__name__} with ID {obj_id} not found")
                    raise ValueError(f"{self.model.__name__} with ID {obj_id} not found")
                    
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                logger.info(f"Updated {self.model.__name__} with ID: {obj_id}")
                return obj
        except Exception as e:
            logger.error(f"Failed to update {self.model.__name__} with ID {obj_id}: {e}", exc_info=True)
            raise
    
    async def get_by(self, id: int) -> Optional[ModelType]:
        """
        Get record by ID.
        Pay attention that id might not suffice to define if two objects in 
        the database are equal. ID might be a surrogate key.
        Use get_by_natural_key instead
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
    @abstractmethod
    async def get_by(self, obj: ModelType) -> Optional[ModelType]:
        """
        Get existing record by natural/business key (not database ID).
        
        Each subclass defines what makes an object "the same" in business terms.
        Examples:
        - Article: same original_url
        - Review: same id (business ID from source)
        - User: same telegram_id
        
        Args:
            obj: Model instance with natural key fields populated
            
        Returns:
            Existing model instance or None
        """
        pass
    
    async def exists(self, obj: ModelType) -> bool:
        """
        Check if record exists by natural key.
        
        Args:
            obj: Model instance with natural key fields populated
            
        Returns:
            True if exists, False otherwise
        """
        logger.debug(f"Checking if {self.model.__name__} exists by natural key")
        existing = await self.get_by(obj)
        exists = existing is not None
        logger.debug(f"{self.model.__name__} exists by natural key: {exists}")
        return exists
    
    async def exists(self, id: int) -> bool:
        """
        Check if record exists.
        
        Pay attention that id might not suffice to define if two objects in 
        the database are equal. ID might be a surrogate key.
        Use exists_by_natural_key instead
        
        Args:
            id: Primary key value
            
        Returns:
            True if exists, False otherwise
        """
        logger.debug(f"Checking if {self.model.__name__} exists with ID: {id}")
        obj = await self.get_by(id)
        exists = obj is not None
        logger.debug(f"{self.model.__name__} with ID {id} exists: {exists}")
        return exists
    
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
        
    def _get_identifier_for_logging(self, obj: ModelType, existing: ModelType = None) -> str:
        """
        Get a meaningful identifier for logging.
        Override in subclasses for better messages.
        
        Args:
            obj: The object being saved
            existing: The existing object found (if any)
            
        Returns:
            String identifier for logging
        """
        target = existing if existing else obj
        if hasattr(target, 'id') and target.id is not None:
            return f"ID={target.id}"
        return "natural key"
    