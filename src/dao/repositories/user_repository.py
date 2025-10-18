from typing import Optional, List
from sqlmodel import select

from src.dao.models.user import User
from src.dao.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model with domain-specific queries"""
    
    def __init__(self):
        super().__init__(User)
    
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """
        Get user by Telegram ID.
        
        Args:
            telegram_id: User's Telegram ID
            
        Returns:
            User instance or None
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Telegram username
            
        Returns:
            User instance or None
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(User).where(User.username == username)
            )
            return result.scalar_one_or_none()
    
    async def get_all_admins(self) -> List[User]:
        """
        Get all admin users.
        
        Returns:
            List of admin users
        """
        async with self.db.get_async_session() as session:
            result = await session.execute(
                select(User).where(User.is_admin == True)
            )
            return result.scalars().all()
    
    async def create_user(
        self,
        telegram_id: int,
        username: str,
        first_name: str,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        is_admin: bool = True
    ) -> User:
        """
        Create a new user.
        
        Args:
            telegram_id: Telegram user ID
            username: Telegram username
            first_name: User's first name
            last_name: User's last name (optional)
            phone: User's phone (optional)
            is_admin: Admin status (default: True)
            
        Returns:
            Created User instance
        """
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            is_admin=is_admin
        )
        return await self.create(user)
    
    async def update_admin_status(self, telegram_id: int, is_admin: bool) -> Optional[User]:
        """
        Update user's admin status.
        
        Args:
            telegram_id: User's Telegram ID
            is_admin: New admin status
            
        Returns:
            Updated User or None if not found
        """
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.is_admin = is_admin
            return await self.update(user)
        return None


# Singleton instance
user_repository = UserRepository()