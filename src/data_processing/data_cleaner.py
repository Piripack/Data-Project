import pandas as pd

class DataCleaner:
    def __init__(self, database):
        self.database = database

    def load_user_data(self):
        """Load data from database"""
        return self.database.load_user_data()

    def clean_user_data(self, data):
        """Clean the user data"""
        if data is None:
            return None

        # Create a copy of the data
        cleaned_data = data.copy()

        # Sort by creation date
        cleaned_data = cleaned_data.sort_values('created_at')

        # Remove any duplicates
        cleaned_data = cleaned_data.drop_duplicates()

        # Reset index
        cleaned_data = cleaned_data.reset_index(drop=True)

        return cleaned_data