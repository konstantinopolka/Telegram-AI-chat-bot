"""change id to id

Revision ID: fa1f25120ddb
Revises: 557814eea3f9
Create Date: 2025-11-10 19:55:40.427112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
# revision identifiers, used by Alembic.
revision: str = 'fa1f25120ddb'
down_revision: Union[str, Sequence[str], None] = '557814eea3f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # For SQLite, renaming primary key columns requires table recreation
    
    # Check current state
    from alembic import context
    bind = context.get_bind()
    inspector = sa.inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('reposting_bot_users')]
    
    # Determine which column has the data
    source_column = 'id' if 'id' in columns else 'id'
    
    # Create new table with correct schema
    op.execute('''
        CREATE TABLE reposting_bot_users_new (
            id INTEGER NOT NULL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50),
            phone VARCHAR(20),
            is_admin BOOLEAN NOT NULL,
            registered_at DATETIME NOT NULL
        )
    ''')
    
    # Copy data from old table
    op.execute(f'''
        INSERT INTO reposting_bot_users_new (id, username, first_name, last_name, phone, is_admin, registered_at)
        SELECT {source_column}, username, first_name, last_name, phone, is_admin, registered_at
        FROM reposting_bot_users
    ''')
    
    # Replace old table
    op.execute('DROP TABLE reposting_bot_users')
    op.execute('ALTER TABLE reposting_bot_users_new RENAME TO reposting_bot_users')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # Reverse: rename id back to id
    op.execute('''
        CREATE TABLE reposting_bot_users_new (
            id INTEGER NOT NULL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50),
            phone VARCHAR(20),
            is_admin BOOLEAN NOT NULL,
            registered_at DATETIME NOT NULL
        )
    ''')
    
    op.execute('''
        INSERT INTO reposting_bot_users_new (id, username, first_name, last_name, phone, is_admin, registered_at)
        SELECT id, username, first_name, last_name, phone, is_admin, registered_at
        FROM reposting_bot_users
    ''')
    
    op.execute('DROP TABLE reposting_bot_users')
    op.execute('ALTER TABLE reposting_bot_users_new RENAME TO reposting_bot_users')
    # ### end Alembic commands ###
