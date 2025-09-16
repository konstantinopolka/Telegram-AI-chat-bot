#!/usr/bin/env python3
"""
Post-write hook for Alembic to automatically remove unused sqlmodel imports
from generated migration files.
"""
import sys
import re

def clean_sqlmodel_import(filename):
    """Remove sqlmodel import if it's not used in the migration file."""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Check if sqlmodel is actually used in the migration
    # Look for patterns like sqlmodel.sql.sqltypes or sqlmodel.
    sqlmodel_usage_patterns = [
        r'sqlmodel\.sql\.sqltypes',
        r'sqlmodel\.sql\.',
        r'sqlmodel\.Column',
        r'sqlmodel\.String',
        r'sqlmodel\.Integer',
        r'sqlmodel\.DateTime',
        r'sqlmodel\.JSON',
        r'sqlmodel\.Text',
        r'sqlmodel\.Boolean',
        # Add more patterns as needed
    ]
    
    # Check if any of these patterns are found in the migration
    sqlmodel_used = any(re.search(pattern, content) for pattern in sqlmodel_usage_patterns)
    
    if not sqlmodel_used:
        # Remove the sqlmodel import line
        content = re.sub(r'^import sqlmodel\s*\n', '', content, flags=re.MULTILINE)
        
        # Write the cleaned content back
        with open(filename, 'w') as f:
            f.write(content)
        
        print(f"Removed unused sqlmodel import from {filename}")
    else:
        print(f"Kept sqlmodel import in {filename} (it's being used)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sqlmodel_import_cleaner.py <migration_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    clean_sqlmodel_import(filename)
