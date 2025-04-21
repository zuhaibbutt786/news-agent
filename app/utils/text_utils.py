import re
import unicodedata
import random
import string

def generate_slug(text):
    """
    Generate a URL-friendly slug from the given text.
    
    Args:
        text (str): The text to convert to a slug
        
    Returns:
        str: A URL-friendly slug
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove accents
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    
    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    
    # Remove leading/trailing hyphens
    text = text.strip('-')
    
    # Ensure slug is not empty
    if not text:
        # Generate a random string if the slug is empty
        text = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    return text

def truncate_text(text, max_length=100, suffix='...'):
    """
    Truncate text to a specified maximum length.
    
    Args:
        text (str): The text to truncate
        max_length (int): Maximum length of the truncated text
        suffix (str): String to append to truncated text
        
    Returns:
        str: Truncated text
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length-len(suffix)] + suffix

def format_date(date_obj, format_str='%B %d, %Y'):
    """
    Format a datetime object as a string.
    
    Args:
        date_obj (datetime): The datetime object to format
        format_str (str): The format string
        
    Returns:
        str: Formatted date string
    """
    if not date_obj:
        return ""
    
    return date_obj.strftime(format_str)

def html_to_text(html):
    """
    Convert HTML to plain text.
    
    Args:
        html (str): HTML content
        
    Returns:
        str: Plain text
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html)
    
    # Replace HTML entities
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&quot;', '"', text)
    text = re.sub(r'&#39;', "'", text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()