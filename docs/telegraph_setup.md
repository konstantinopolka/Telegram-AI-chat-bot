# Telegraph Configuration Setup

## Overview

The Telegraph configuration has been moved from `graph_bot.json` to environment variables for better security. The sensitive Telegraph access token and configuration are now stored in the `.env` file.

## Environment Variables

Add these variables to your `.env` file:

```properties
# Telegraph Configuration
TELEGRAPH_ACCESS_TOKEN=your_telegraph_access_token_here
TELEGRAPH_SHORT_NAME=konstantinopolka
TELEGRAPH_AUTHOR_NAME=Platypus Review
TELEGRAPH_AUTHOR_URL=https://platypus1917.org/platypus-review/
TELEGRAPH_AUTH_URL=https://edit.telegra.ph/auth/your_auth_url_here
```

## Usage

### Basic Usage

```python
from src.telegraph_manager import TelegraphManager

# The TelegraphManager will automatically load from environment variables
telegraph_manager = TelegraphManager()

# Or you can still provide an access token directly
telegraph_manager = TelegraphManager(access_token="your_token")
```

### In Tests

```python
import os
from src.telegraph_manager import TelegraphManager

# Load from environment
telegraph_manager = TelegraphManager()

# Or use a test token
telegraph_manager = TelegraphManager(access_token="test_token")
```

## Migration from JSON

The system maintains backward compatibility with `graph_bot.json`:

1. **Priority Order**: Environment variables take precedence over JSON file
2. **Fallback**: If no environment variables are found, it will try to load from `graph_bot.json`
3. **New Account**: If neither source is available, a new Telegraph account will be created

## Security Benefits

- ✅ Sensitive tokens are no longer committed to version control
- ✅ Different environments can have different configurations
- ✅ Access tokens are kept in secure environment variables
- ✅ Backward compatibility maintained for existing setups

## Troubleshooting

If you encounter issues:

1. Verify `.env` file exists and contains `TELEGRAPH_ACCESS_TOKEN`
2. Check that the access token is valid and not expired
3. Ensure the `.env` file is loaded before creating TelegraphManager instances
4. For tests, make sure the test environment has access to the variables or uses test tokens
