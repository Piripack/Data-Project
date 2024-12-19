import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats

class UserAnalytics:
    def __init__(self, data):
        self.data = data
        self.analysis_timestamp = datetime.now()

    def get_age_analysis(self):
        """Analyze age distribution and statistics"""
        age_analysis = {
            'basic_stats': {
                'mean_age': self.data['age'].mean(),
                'median_age': self.data['age'].median(),
                'age_std': self.data['age'].std(),
                'youngest': self.data['age'].min(),
                'oldest': self.data['age'].max()
            },
            'age_groups': self.data['age'].value_counts().sort_index().to_dict(),
            'age_distribution': {
                'skewness': stats.skew(self.data['age']),
                'kurtosis': stats.kurtosis(self.data['age'])
            }
        }
        return age_analysis

    def get_location_analysis(self):
        """Analyze user geographical distribution"""
        location_analysis = {
            'location_counts': self.data['location'].value_counts().to_dict(),
            'location_groups': self.data['location_group'].value_counts().to_dict(),
            'age_by_location': self.data.groupby('location')['age'].mean().to_dict()
        }
        return location_analysis

    def get_registration_analysis(self):
        """Analyze user registration patterns"""
        self.data['registration_hour'] = pd.to_datetime(self.data['created_at']).dt.hour
        self.data['registration_day'] = pd.to_datetime(self.data['created_at']).dt.day_name()

        registration_analysis = {
            'total_users': len(self.data),
            'registrations_by_hour': self.data['registration_hour'].value_counts().sort_index().to_dict(),
            'registrations_by_day': self.data['registration_day'].value_counts().to_dict(),
            'average_account_age': self.data['account_age_days'].mean()
        }
        return registration_analysis

    def generate_full_report(self):
        """Generate a comprehensive analysis report"""
        return {
            'timestamp': self.analysis_timestamp,
            'age_analysis': self.get_age_analysis(),
            'location_analysis': self.get_location_analysis(),
            'registration_analysis': self.get_registration_analysis()
        }