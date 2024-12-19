import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.database import Database
from src.utils.helpers import validate_user_input

def test_database():
    # Initialize database
    db = Database()
    
    # Test user creation
    test_user = {
        'first_name': 'John',
        'last_name': 'Doe',
        'date_of_birth': '1990-01-01',
        'location': 'New York',
        'username': 'johndoe',
        'password': 'test123'
    }
    
    # Validate input
    errors = validate_user_input(**test_user)
    if errors:
        print("Validation errors:", errors)
        return
    
    # Add user
    success = db.add_user(**test_user)
    if success:
        print("User added successfully!")
    else:
        print("Failed to add user (username might already exist)")
    
    # Test login
    if db.validate_login('johndoe', 'test123'):
        print("Login successful!")
    else:
        print("Login failed!")
    
    # Get user details
    user = db.get_user('johndoe')
    if user:
        print("User found:", user)
    
    db.close()

if __name__ == "__main__":
    test_database()