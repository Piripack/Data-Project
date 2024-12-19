from datetime import datetime

def get_current_utc():
    """Get current UTC time in formatted string"""
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

def format_datetime(dt):
    """Format a datetime object to string"""
    return dt.strftime('%Y-%m-%d %H:%M:%S')