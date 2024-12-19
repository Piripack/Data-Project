import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.database import Database
from src.data_processing.data_cleaner import DataCleaner
from src.data_processing.feature_engineering import FeatureEngineer

def test_data_processing():
    # Initialize database and add some test users
    db = Database()
    
    # Add more test users for better analysis
    test_users = [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '1990-01-01',
            'location': 'New York',
            'username': 'johndoe',
            'password': 'test123'
        },
        {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': '1995-05-15',
            'location': 'London',
            'username': 'janesmith',
            'password': 'test456'
        }
    ]
    
    for user in test_users:
        db.add_user(**user)
    
    # Initialize data cleaner and feature engineer
    cleaner = DataCleaner(db)
    engineer = FeatureEngineer()
    
    # Load and clean data
    raw_data = cleaner.load_user_data()
    if raw_data is not None:
        print("\nRaw Data Shape:", raw_data.shape)
        
        # Clean data
        cleaned_data = cleaner.clean_user_data(raw_data)
        print("\nCleaned Data Sample:")
        print(cleaned_data.head())
        
        # Get data quality report
        quality_report = cleaner.get_data_quality_report(cleaned_data)
        print("\nData Quality Report:")
        print(quality_report)
        
        # Create enhanced features
        enhanced_data = engineer.create_user_features(cleaned_data)
        print("\nEnhanced Data Columns:")
        print(enhanced_data.columns.tolist())
        print("\nEnhanced Data Sample:")
        print(enhanced_data.head())
    
    db.close()

if __name__ == "__main__":
    test_data_processing()