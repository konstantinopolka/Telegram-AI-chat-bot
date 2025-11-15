import os
from dotenv import load_dotenv

load_dotenv()
# Parse admin lists from environment variables
def _parse_admin_ids() -> list[int]:
    """Parse comma-separated admin IDs from environment"""
    ids_str = os.getenv('ADMIN_IDS', '')
    return [int(id.strip()) for id in ids_str.split(',') if id.strip().isdigit()]

def _parse_admin_nicknames() -> list[str]:
    """Parse comma-separated admin usernames from environment"""
    nicknames_str = os.getenv('ADMIN_NICKNAMES', '')
    return [name.strip().lower() for name in nicknames_str.split(',') if name.strip()]

ADMIN_IDS = _parse_admin_ids()
ADMIN_NICKNAMES = _parse_admin_nicknames()