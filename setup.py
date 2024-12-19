import os
import sys

def check_setup():
    """Check if all necessary files and directories exist"""
    required_files = [
        'src/utils/__init__.py',
        'src/utils/database.py',
        'src/data_processing/__init__.py',
        'src/data_processing/data_cleaner.py',
        'src/data_processing/feature_engineering.py',
        'src/visualization/__init__.py',
        'src/visualization/dashboard.py',
        'web_app/templates/index.html'
    ]

    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ Found {file_path}")
        else:
            print(f"✗ Missing {file_path}")

    try:
        import pandas
        print("✓ pandas is installed")
    except ImportError:
        print("✗ pandas is not installed")

    try:
        import numpy
        print("✓ numpy is installed")
    except ImportError:
        print("✗ numpy is not installed")

    try:
        import plotly
        print("✓ plotly is installed")
    except ImportError:
        print("✗ plotly is not installed")

if __name__ == "__main__":
    check_setup()