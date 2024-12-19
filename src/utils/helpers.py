from datetime import datetime

def validate_date_format(date_string):
    """Validate if a string is in YYYY-MM-DD format"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_user_input(first_name, last_name, date_of_birth, location, username, password):
    """Validate user input data"""
    errors = []
    
    if not first_name or len(first_name) < 2:
        errors.append("First name must be at least 2 characters long")
    
    if not last_name or len(last_name) < 2:
        errors.append("Last name must be at least 2 characters long")
    
    if not validate_date_format(date_of_birth):
        errors.append("Date of birth must be in YYYY-MM-DD format")
    
    if not location or len(location) < 2:
        errors.append("Location must be at least 2 characters long")
    
    if not username or len(username) < 4:
        errors.append("Username must be at least 4 characters long")
    
    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters long")
    
    return errors