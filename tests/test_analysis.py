import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.database import Database
from src.data_processing.data_cleaner import DataCleaner
from src.data_processing.feature_engineering import FeatureEngineer
from src.analysis.advanced_analytics import UserAnalytics
from src.analysis.statistical_analysis import StatisticalAnalyzer

def add_test_users(db):
    """Add test users to the database"""
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
        },
        {
            'first_name': 'Mike',
            'last_name': 'Johnson',
            'date_of_birth': '1988-03-20',
            'location': 'Paris',
            'username': 'mikej',
            'password': 'test789'
        },
        {
            'first_name': 'Sarah',
            'last_name': 'Williams',
            'date_of_birth': '1992-11-08',
            'location': 'Berlin',
            'username': 'sarahw',
            'password': 'test012'
        },
        {
            'first_name': 'David',
            'last_name': 'Brown',
            'date_of_birth': '1985-07-22',
            'location': 'New York',
            'username': 'davidb',
            'password': 'test345'
        }
    ]
    
    for user in test_users:
        db.add_user(**user)

def test_analysis():
    # Initialize database
    db = Database()
    
    # Add test users
    add_test_users(db)
    
    # Initialize components
    cleaner = DataCleaner(db)
    engineer = FeatureEngineer()
    
    # Load and process data
    raw_data = cleaner.load_user_data()
    if raw_data is not None:
        cleaned_data = cleaner.clean_user_data(raw_data)
        enhanced_data = engineer.create_user_features(cleaned_data)
        
        # Initialize analytics
        user_analytics = UserAnalytics(enhanced_data)
        statistical_analyzer = StatisticalAnalyzer(enhanced_data)
        
        # Generate reports
        print("\nUser Analytics Report:")
        print("-" * 50)
        full_report = user_analytics.generate_full_report()
        for section, data in full_report.items():
            if section != 'timestamp':
                print(f"\n{section.replace('_', ' ').title()}:")
                for key, value in data.items():
                    print(f"{key}: {value}")
        
        print("\nStatistical Analysis:")
        print("-" * 50)
        
        print("\nAge Normality Test:")
        normality_test = statistical_analyzer.test_age_normality()
        for key, value in normality_test.items():
            print(f"{key}: {value}")
        
        print("\nAge Comparison by Location Group:")
        group_comparison = statistical_analyzer.compare_groups('age', 'location_group')
        for key, value in group_comparison.items():
            print(f"{key}: {value}")
        
        print("\nCorrelation Analysis:")
        correlations = statistical_analyzer.correlation_analysis()
        for var1, corrs in correlations.items():
            if isinstance(corrs, dict):
                print(f"\nCorrelations for {var1}:")
                for var2, corr in corrs.items():
                    if corr is not None:
                        print(f"  with {var2}: {corr:.2f}")
    
    db.close()

if __name__ == "__main__":
    test_analysis()