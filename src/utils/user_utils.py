class UserSession:
    @staticmethod
    def get_current_user():
        """Get current user's login name"""
        return "Piripack"

    @staticmethod
    def get_user_info():
        """Get additional user information"""
        return {
            'username': 'Piripack',
            'role': 'User',
            'last_login': '2024-12-19 10:41:12'
        }