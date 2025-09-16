#!/usr/bin/env python3
"""
Setup script for Telegraph integration tests.
Creates a Telegraph account and saves the token for testing.
"""
import os
import json
from telegraph import Telegraph

def setup_telegraph_account():
    """Create a Telegraph account for testing and save credentials."""
    try:
        # Create Telegraph instance
        telegraph = Telegraph()
        
        # Create account
        account_data = telegraph.create_account(
            short_name='test_bot',
            author_name='Test Bot',
            author_url='https://test.example.com'
        )
        
        print("✅ Telegraph account created successfully!")
        print(f"   Access Token: {account_data['access_token']}")
        print(f"   Author Name: {account_data['author_name']}")
        print(f"   Author URL: {account_data.get('author_url', 'N/A')}")
        
        # Save to file
        token_file = 'graph_bot.json'
        with open(token_file, 'w') as f:
            json.dump(account_data, f, indent=2)
        
        # Also export as environment variable for the session
        os.environ['TELEGRAPH_ACCESS_TOKEN'] = account_data['access_token']
        
        print(f"✅ Credentials saved to {token_file}")
        print("✅ Environment variable TELEGRAPH_ACCESS_TOKEN set for this session")
        
        return account_data['access_token']
        
    except Exception as e:
        print(f"❌ Failed to create Telegraph account: {e}")
        return None

if __name__ == "__main__":
    setup_telegraph_account()