"""
Constants for HTML content cleaning and parsing operations.
"""

# HTML tags allowed in cleaned content for Telegraph compatibility
ALLOWED_TAGS = {
    'a', 'b', 'i', 'em', 'strong', 'u', 's', 'blockquote',
    'code', 'pre', 'p', 'ul', 'ol', 'li', 'br', 'hr', 'img'
}

# CSS selectors for irrelevant content that should be removed
IRRELEVANT_INFO_TAGS = 'nav, footer, .sidebar, script, style, .comments'

# Required fields for content validation
REQUIRED_FIELDS = ['title', 'content', 'original_url']

# Minimum title length for validation
MIN_TITLE_LENGTH = 5

# Minimum content length for validation
MIN_CONTENT_LENGTH = 100