from typing import Generic, TypeVar, Optional, List, Type
from sqlmodel import SQLModel, select
from sqlalchemy import func

from src.dao.core.database_manager import db_manager

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
    
    async def create(self, obj: ModelType) -> ModelType:
        """
        Create a new record.
        
        Args:
            obj: Model instance to create
            
        Returns:
            Created model instance with ID populated
        """
        async with self.db.get_async_session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
    
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get record by ID.
        
        Args:
            id: Primary key value
            
        Returns:
            Model instance or None if not found
        """
        async with self.db.get_async_session() as session:
            return await session.get(self.model, id)
    
    async def get_all(self) -> List[ModelType]:
        """
        Get all records.
        
        Returns:
            List of all model instances
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(select(self.model))
            return result.scalars().all()
    
    async def update(self, obj: ModelType) -> ModelType:
        """
        Update existing record.
        
        Args:
            obj: Model instance with updated values
            
        Returns:
            Updated model instance
        """
        async with self.db.get_async_session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
    
    async def delete(self, id: int) -> bool:
        """
        Delete record by ID.
        
        Args:
            id: Primary key value
            
        Returns:
            True if deleted, False if not found
        """
        async with self.db.get_async_session() as session:
            obj = await session.get(self.model, id)
            if obj:
                await session.delete(obj)
                await session.commit()
                return True
            return False
    
    async def exists(self, id: int) -> bool:
        """
        Check if record exists.
        
        Args:
            id: Primary key value
            
        Returns:
            True if exists, False otherwise
        """
        obj = await self.get_by_id(id)
        return obj is not None
    
    async def count(self) -> int:
        """
        Count total records.
        
        Returns:
            Total number of records
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(self.model).with_only_columns(func.count())
            )
            return result.scalar()