from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, email, password, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get(user_id):
        """Retrieve user by ID"""
        return users.get(user_id)

# Initialize users dictionary
users = {}

# Add admin user
admin_user = User(
    id=1, 
    username="admin", 
    email="admin@example.com", 
    password="admin", 
    is_admin=True
)

# Add regular user (Piripack)
piripack_user = User(
    id=2,
    username="Piripack",
    email="piripack@example.com",
    password="123",  # Change this to a secure password
    is_admin=False
)

# Add users to the dictionary using username as key
users["admin"] = admin_user
users["Piripack"] = piripack_user

# Also store users by ID for the user loader
users_by_id = {
    str(admin_user.id): admin_user,
    str(piripack_user.id): piripack_user
}

def get_user_by_id(user_id):
    """Helper function to get user by ID"""
    return users_by_id.get(str(user_id))

def get_user_by_username(username):
    """Helper function to get user by username"""
    return users.get(username)