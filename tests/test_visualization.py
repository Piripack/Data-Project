import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.database import Database
from src.data_processing.data_cleaner import DataCleaner
from src.data_processing.feature_engineering import FeatureEngineer
from src.visualization.dashboard import Dashboard


def test_visualization():
    # Initialize database and get processed data
    db = Database()
    cleaner = DataCleaner(db)
    engineer = FeatureEngineer()

    # Load and process data
    raw_data = cleaner.load_user_data()
    if raw_data is not None:
        cleaned_data = cleaner.clean_user_data(raw_data)
        enhanced_data = engineer.create_user_features(cleaned_data)

        # Create dashboard
        dashboard = Dashboard(enhanced_data)

        # Ensure directory exists
        os.makedirs("web_app/static/plots", exist_ok=True)

        # Generate and save all plots
        plots = dashboard.create_dashboard()

        # Print confirmation
        for name in plots.keys():
            print(f"Created visualization: {name}")

    db.close()


if __name__ == "__main__":
    test_visualization()