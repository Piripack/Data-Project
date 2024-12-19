import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sys
from datetime import datetime
import os
import importlib
import sqlite3
import json


class SystemTester:
    def __init__(self):
        self.results = {
            "passed": [],
            "failed": [],
            "skipped": [],
            "warnings": []
        }
        self.driver = None
        self.expected_files = [
            'app.py',
            'requirements.txt',
            'README.md',
            'web_app/templates/index.html',
            'web_app/templates/login.html',
            'web_app/static/css/style.css',
            'web_app/static/js/main.js',
            'src/models/user.py',
            'src/utils/database.py',
            'src/data_processing/data_cleaner.py',
            'src/data_processing/feature_engineering.py',
            'src/visualization/dashboard.py'
        ]
        self.required_packages = [
            'flask',
            'flask-login',
            'selenium',
            'requests',
            'pandas',
            'numpy',
            'plotly',
            'sqlite3'
        ]

    def log_result(self, test_name, passed, error=None, skipped=False, warning=False):
        if warning:
            self.results["warnings"].append(f"{test_name} - Warning: {error}")
            print(f"⚠️ {test_name}: Warning - {error}")
        elif skipped:
            self.results["skipped"].append(f"{test_name} - Skipped due to: {error}")
            print(f"⚠️ {test_name}: Skipped - {error}")
        elif passed:
            self.results["passed"].append(test_name)
            print(f"✅ {test_name}: Passed")
        else:
            self.results["failed"].append(f"{test_name} - Error: {error}")
            print(f"❌ {test_name}: Failed - {error}")

    def check_project_structure(self):
        """Test 1: Check if all required files exist"""
        missing_files = []
        for file_path in self.expected_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)

        if missing_files:
            self.log_result("Project Structure", False, f"Missing files: {', '.join(missing_files)}")
            return False
        self.log_result("Project Structure", True)
        return True

    def check_dependencies(self):
        """Test 2: Check if all required packages are installed"""
        missing_packages = []
        for package in self.required_packages:
            try:
                importlib.import_module(package.replace('-', '_'))
            except ImportError:
                missing_packages.append(package)

        if missing_packages:
            self.log_result("Dependencies", False, f"Missing packages: {', '.join(missing_packages)}")
            return False
        self.log_result("Dependencies", True)
        return True

    def check_database(self):
        """Test 3: Check database connection and tables"""
        try:
            conn = sqlite3.connect('instance/data.db')
            cursor = conn.cursor()

            # Check if required tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            expected_tables = ['user', 'data']  # Add your expected tables
            missing_tables = [table for table in expected_tables if (table,) not in tables]

            if missing_tables:
                self.log_result("Database Structure", False, f"Missing tables: {', '.join(missing_tables)}")
                return False

            self.log_result("Database Structure", True)
            return True
        except Exception as e:
            self.log_result("Database Structure", False, f"Database error: {str(e)}")
            return False

    def test_server_connection(self):
        """Test 4: Check if server is running and responding"""
        try:
            response = requests.get('http://127.0.0.1:5000')

            # Check response status
            if response.status_code != 200:
                self.log_result("Server Connection", False, f"Server returned status code: {response.status_code}")
                return False

            # Check if response contains expected elements
            if 'Current Date and Time (UTC):' not in response.text:
                self.log_result("Server Response", False, "Missing time display")
                return False

            if 'Current User\'s Login: Piripack' not in response.text:
                self.log_result("Server Response", False, "Missing username display")
                return False

            self.log_result("Server Connection", True)
            return True
        except requests.exceptions.ConnectionError as e:
            self.log_result("Server Connection", False, f"Cannot connect to server: {str(e)}")
            return False

    def test_ui_elements(self):
        """Test 5: Check UI elements and their functionality"""
        try:
            if not self.driver:
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')  # Run in headless mode
                self.driver = webdriver.Chrome(options=options)

            self.driver.get('http://127.0.0.1:5000')

            # Check time format
            time_element = self.driver.find_element(By.CLASS_NAME, "text-white")
            time_text = time_element.text
            try:
                datetime.strptime(time_text.split(': ')[1], '%Y-%m-%d %H:%M:%S')
            except:
                self.log_result("Time Format", False, "Invalid time format")
                return False

            # Check navigation elements
            nav_elements = {
                "navbar-brand": "Data Analysis Dashboard",
                "text-white": ["Current Date and Time (UTC):", "Current User's Login:"],
                "btn-light": "Logout"
            }

            for class_name, expected_text in nav_elements.items():
                elements = self.driver.find_elements(By.CLASS_NAME, class_name)
                if not elements:
                    self.log_result("UI Elements", False, f"Missing element with class: {class_name}")
                    return False

                if isinstance(expected_text, list):
                    found_texts = [e.text for e in elements]
                    for text in expected_text:
                        if not any(text in ft for ft in found_texts):
                            self.log_result("UI Elements", False, f"Missing text: {text}")
                            return False
                else:
                    if not any(expected_text in e.text for e in elements):
                        self.log_result("UI Elements", False, f"Missing text: {expected_text}")
                        return False

            self.log_result("UI Elements", True)
            return True
        except Exception as e:
            self.log_result("UI Elements", False, str(e))
            return False

    def test_data_processing(self):
        """Test 6: Check data processing functionality"""
        try:
            # Import and test data processing modules
            from src.data_processing.data_cleaner import DataCleaner
            from src.data_processing.feature_engineering import FeatureEngineer

            # Test with sample data
            sample_data = {'column1': [1, 2, 3], 'column2': [4, 5, 6]}

            cleaner = DataCleaner()
            engineer = FeatureEngineer()

            # Test basic functionality
            cleaned_data = cleaner.clean_data(sample_data)
            processed_data = engineer.process_data(cleaned_data)

            if cleaned_data is None or processed_data is None:
                self.log_result("Data Processing", False, "Data processing returned None")
                return False

            self.log_result("Data Processing", True)
            return True
        except Exception as e:
            self.log_result("Data Processing", False, f"Data processing error: {str(e)}")
            return False

    def test_visualization(self):
        """Test 7: Check visualization functionality"""
        try:
            plot_files = os.listdir('web_app/static/plots')
            if not plot_files:
                self.log_result("Visualization", False, "No plot files found")
                return False

            self.log_result("Visualization", True)
            return True
        except Exception as e:
            self.log_result("Visualization", False, str(e))
            return False

    def print_summary(self):
        """Print test results summary"""
        print("\n=== Test Summary ===")
        total = len(self.results['passed']) + len(self.results['failed']) + len(self.results['skipped'])
        print(f"Total Tests: {total}")
        print(f"Passed: {len(self.results['passed'])}")
        print(f"Failed: {len(self.results['failed'])}")
        print(f"Skipped: {len(self.results['skipped'])}")
        print(f"Warnings: {len(self.results['warnings'])}")

        if self.results['failed']:
            print("\nFailed Tests:")
            for failure in self.results['failed']:
                print(f"- {failure}")

        if self.results['warnings']:
            print("\nWarnings:")
            for warning in self.results['warnings']:
                print(f"- {warning}")

        if self.results['skipped']:
            print("\nSkipped Tests:")
            for skipped in self.results['skipped']:
                print(f"- {skipped}")

        # Generate report file
        report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'results': self.results,
            'summary': {
                'total': total,
                'passed': len(self.results['passed']),
                'failed': len(self.results['failed']),
                'skipped': len(self.results['skipped']),
                'warnings': len(self.results['warnings'])
            }
        }

        with open('test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print("\nDetailed test report saved to test_report.json")

    def run_all_tests(self):
        """Run all system tests"""
        print("\n=== System Functionality Test ===\n")

        tests = [
            (self.check_project_structure, "Project Structure Check"),
            (self.check_dependencies, "Dependencies Check"),
            (self.check_database, "Database Check"),
            (self.test_server_connection, "Server Connection Check"),
            (self.test_ui_elements, "UI Elements Check"),
            (self.test_data_processing, "Data Processing Check"),
            (self.test_visualization, "Visualization Check")
        ]

        for test_func, test_name in tests:
            try:
                print(f"\nRunning {test_name}...")
                test_func()
            except Exception as e:
                self.log_result(test_name, False, f"Unexpected error: {str(e)}")
                print(f"Stack trace for {test_name}:")
                import traceback
                print(traceback.format_exc())

        if self.driver:
            self.driver.quit()

        self.print_summary()


if __name__ == "__main__":
    tester = SystemTester()
    tester.run_all_tests()