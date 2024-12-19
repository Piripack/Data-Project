import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.database import Database
from src.data_processing.data_cleaner import DataCleaner
from src.data_processing.feature_engineering import FeatureEngineer
from src.analysis.advanced_analytics import UserAnalytics
from src.analysis.statistical_analysis import StatisticalAnalyzer

def test_analysis():
    # Initialize database and get processed data
    db = Database()
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
                print(data)
        
        print("\nStatistical Analysis:")
        print("-" * 50)
        print("\nAge Normality Test:")
        print(statistical_analyzer.test_age_normality())
        
        print("\nAge Comparison by Location Group:")
        print(statistical_analyzer.compare_groups('age', 'location_group'))
        
        print("\nCorrelation Analysis:")
        print(statistical_analyzer.correlation_analysis())
    
    db.close()

if __name__ == "__main__":
    test_analysis()