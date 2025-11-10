# scripts/manage_admins.py
import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.dao.repositories import user_repository
from src.logging_config import get_logger

logger = get_logger(__name__)

async def grant_admin(identifier: str):
    """
    Grant admin rights to a user by Telegram ID or username.
    
    Args:
        identifier: Either a Telegram ID (numeric) or username (with or without @)
    """
    user = None
    
    # Try to parse as Telegram ID (numeric)
    if identifier.isdigit():
        id = int(identifier)
        logger.info(f"Looking up user by Telegram ID: {id}")
        user = await user_repository.get_by_id(id)
    else:
        # Treat as username
        username = identifier.lstrip('@')  # Remove @ if present
        logger.info(f"Looking up user by username: {username}")
        user = await user_repository.get_by_username(username)
    
    if user:
        logger.info(f"User ID: {user.id} ")
        user.is_admin = True
        await user_repository.update(user)
        display_name = user.username or user.first_name or f"ID:{user.id}"
        print(f"✅ Admin rights granted to {display_name} (Telegram ID: {user.id})")
        logger.info(f"Admin rights granted to user {user.id}")
    else:
        print(f"❌ User not found: {identifier}")
        logger.warning(f"User not found: {identifier}")

async def revoke_admin(identifier: str):
    """
    Revoke admin rights from a user by Telegram ID or username.
    
    Args:
        identifier: Either a Telegram ID (numeric) or username (with or without @)
    """
    user = None
    
    if identifier.isdigit():
        id = int(identifier)
        logger.info(f"Looking up user by Telegram ID: {id}")
        user = await user_repository.get_by_id(id)
    else:
        username = identifier.lstrip('@')
        logger.info(f"Looking up user by username: {username}")
        user = await user_repository.get_by_username(username)
    
    if user:
        user.is_admin = False
        await user_repository.update(user)
        display_name = user.username or user.first_name or f"ID:{user.id}"
        print(f"✅ Admin rights revoked from {display_name} (Telegram ID: {user.id})")
        logger.info(f"Admin rights revoked from user {user.id}")
    else:
        print(f"❌ User not found: {identifier}")
        logger.warning(f"User not found: {identifier}")

async def list_admins():
    """List all users with admin rights."""
    # Note: You may need to add this method to user_repository
    logger.info("Listing all admins")
    print("📋 Listing all admins...")
    print("⚠️  Note: list_admins method needs to be implemented in user_repository")
    # admins = await user_repository.get_all_admins()
    # for admin in admins:
    #     display_name = admin.username or admin.first_name
    #     print(f"  • {display_name} (ID: {admin.id})")

if __name__ == "__main__":
    print("=== Admin Management Script ===")
    print("1. Grant admin rights")
    print("2. Revoke admin rights")
    print("3. List all admins")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        identifier = input("Enter Telegram ID or username (@username or username): ").strip()
        asyncio.run(grant_admin(identifier))
    elif choice == "2":
        identifier = input("Enter Telegram ID or username (@username or username): ").strip()
        asyncio.run(revoke_admin(identifier))
    elif choice == "3":
        asyncio.run(list_admins())
    else:
        print("❌ Invalid option")