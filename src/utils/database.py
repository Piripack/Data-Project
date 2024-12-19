import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        # Create sample data when database is initialized
        self.data = self.create_sample_data()

    def create_sample_data(self):
        """Create sample user data"""
        np.random.seed(42)
        
        # Generate 1000 sample users
        n_users = 1000
        
        # Create sample data
        data = {
            'user_id': range(1, n_users + 1),
            'age': np.random.normal(30, 10, n_users).astype(int),
            'location': np.random.choice([
                'United States', 'United Kingdom', 'Canada', 'Germany', 
                'France', 'Australia', 'Japan', 'Brazil', 'India'
            ], n_users),
            'created_at': [
                datetime.now() - timedelta(days=np.random.randint(1, 365))
                for _ in range(n_users)
            ]
        }
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Clean up age data (ensure reasonable range)
        df.loc[df['age'] < 18, 'age'] = 18
        df.loc[df['age'] > 80, 'age'] = 80
        
        return df

    def load_user_data(self):
        """Load user data from database"""
        return self.data

    def close(self):
        """Close database connection"""
        pass  # No actual connection to close in this example