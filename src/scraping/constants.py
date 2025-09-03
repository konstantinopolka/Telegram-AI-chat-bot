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
REQUIRED_FIELDS = ['title', 'content', 'original_url']