from typing import Optional, List
from sqlmodel import select

from src.dao.models.user import User
from src.dao.repositories.base_repository import BaseRepository
from src.logging_config import get_logger

logger = get_logger(__name__)


class UserRepository(BaseRepository[User]):
    """Repository for User model with domain-specific queries"""
    
    def __init__(self):
        super().__init__(User)
        logger.info("UserRepository initialized")
    
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """
        Get user by Telegram ID.
        
        Args:
            telegram_id: User's Telegram ID
            
        Returns:
            User instance or None
        """
        logger.debug(f"Fetching user by telegram_id: {telegram_id}")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(User).where(User.telegram_id == telegram_id)
                )
                user = result.scalar_one_or_none()
                if user:
                    logger.debug(f"Found user: {user.username} (telegram_id={telegram_id})")
                else:
                    logger.debug(f"No user found with telegram_id: {telegram_id}")
                return user
        except Exception as e:
            logger.error(f"Failed to fetch user by telegram_id {telegram_id}: {e}", exc_info=True)
            raise
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Telegram username
            
        Returns:
            User instance or None
        """
        logger.debug(f"Fetching user by username: {username}")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(User).where(User.username == username)
                )
                user = result.scalar_one_or_none()
                if user:
                    logger.debug(f"Found user with username: {username}")
                else:
                    logger.debug(f"No user found with username: {username}")
                return user
        except Exception as e:
            logger.error(f"Failed to fetch user by username {username}: {e}", exc_info=True)
            raise
    
    async def get_all_admins(self) -> List[User]:
        """
        Get all admin users.
        
        Returns:
            List of admin users
        """
        logger.debug("Fetching all admin users")
        try:
            async with self.db.get_async_session() as session:
                result = await session.execute(
                    select(User).where(User.is_admin == True)
                )
                admins = result.scalars().all()
                logger.debug(f"Found {len(admins)} admin users")
                return admins
        except Exception as e:
            logger.error(f"Failed to fetch admin users: {e}", exc_info=True)
            raise
    
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
        logger.info(f"Creating new user: {username} (telegram_id={telegram_id}, admin={is_admin})")
        try:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                is_admin=is_admin
            )
            created_user = await self.create(user)
            logger.info(f"Successfully created user: {username} with ID: {created_user.id}")
            return created_user
        except Exception as e:
            logger.error(f"Failed to create user {username}: {e}", exc_info=True)
            raise
    
    async def update_admin_status(self, telegram_id: int, is_admin: bool) -> Optional[User]:
        """
        Update user's admin status.
        
        Args:
            telegram_id: User's Telegram ID
            is_admin: New admin status
            
        Returns:
            Updated User or None if not found
        """
        logger.info(f"Updating admin status for telegram_id {telegram_id} to: {is_admin}")
        try:
            user = await self.get_by_telegram_id(telegram_id)
            if user:
                user.is_admin = is_admin
                updated_user = await self.update(user)
                logger.info(f"Updated admin status for user {user.username} to: {is_admin}")
                return updated_user
            logger.warning(f"Cannot update admin status - user not found: telegram_id={telegram_id}")
            return None
        except Exception as e:
            logger.error(f"Failed to update admin status for telegram_id {telegram_id}: {e}", exc_info=True)
            raise


# Singleton instance
user_repository = UserRepository()
logger.info("UserRepository singleton instance created")