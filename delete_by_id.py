import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.dao.repositories import user_repository
from src.logging_config import get_logger

logger = get_logger(__name__)

async def delete_user(user_id: int):
    """
    Delete a user by their ID.
    
    Args:
        user_id: The user's ID (primary key)
    """
    try:
        user = await user_repository.get_by_id(user_id)
        
        if user:
            display_name = user.username or user.first_name or f"ID:{user.id}"
            # Pass the ID, not the object
            deleted = await user_repository.delete(user_id)
            if deleted:
                print(f"✅ User deleted: {display_name} (ID: {user_id})")
                logger.info(f"User {user_id} deleted successfully")
            else:
                print(f"❌ Failed to delete user: {display_name}")
        else:
            print(f"❌ User not found with ID: {user_id}")
            logger.warning(f"User not found: {user_id}")
            
    except Exception as e:
        print(f"❌ Error deleting user: {e}")
        logger.error(f"Error deleting user {user_id}: {e}", exc_info=True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_id = int(sys.argv[1])
    else:
        user_id = int(input("Enter user ID to delete: "))
    
    asyncio.run(delete_user(user_id))