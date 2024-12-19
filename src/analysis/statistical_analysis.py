import numpy as np
from scipy import stats
import pandas as pd

class StatisticalAnalyzer:
    def __init__(self, data):
        self.data = data
        self.min_samples_for_analysis = 3  # Minimum sample size for statistical tests

    def test_age_normality(self):
        """Test if age distribution is normal"""
        if len(self.data) < self.min_samples_for_analysis:
            return {
                'test_name': "D'Agostino's K^2 Test",
                'message': 'Insufficient data for normality test (need at least 3 samples)',
                'statistic': None,
                'p_value': None,
                'is_normal': None
            }
        
        statistic, p_value = stats.normaltest(self.data['age'])
        return {
            'test_name': "D'Agostino's K^2 Test",
            'message': 'Test completed successfully',
            'statistic': statistic,
            'p_value': p_value,
            'is_normal': p_value > 0.05 if not np.isnan(p_value) else None
        }

    def compare_groups(self, column, group_by):
        """Compare values between different groups"""
        groups = self.data.groupby(group_by)[column].apply(list)
        
        if any(len(group) < 2 for group in groups):
            return {
                'test_name': 'Group Comparison',
                'message': 'Insufficient data in one or more groups (need at least 2 samples per group)',
                'statistic': None,
                'p_value': None,
                'groups': groups.index.tolist()
            }

        if len(groups) == 2:
            # Perform t-test for two groups
            group1, group2 = groups.values
            try:
                statistic, p_value = stats.ttest_ind(group1, group2)
                message = 'Test completed successfully'
            except Exception as e:
                return {
                    'test_name': 'Independent t-test',
                    'message': f'Error performing t-test: {str(e)}',
                    'statistic': None,
                    'p_value': None,
                    'groups': groups.index.tolist()
                }
            test_name = "Independent t-test"
        else:
            # Perform ANOVA for more than two groups
            try:
                statistic, p_value = stats.f_oneway(*groups)
                message = 'Test completed successfully'
            except Exception as e:
                return {
                    'test_name': 'One-way ANOVA',
                    'message': f'Error performing ANOVA: {str(e)}',
                    'statistic': None,
                    'p_value': None,
                    'groups': groups.index.tolist()
                }
            test_name = "One-way ANOVA"

        return {
            'test_name': test_name,
            'message': message,
            'statistic': statistic,
            'p_value': p_value,
            'groups': groups.index.tolist()
        }

    def correlation_analysis(self):
        """Analyze correlations between numeric variables"""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        # Filter out columns with all NaN values
        valid_cols = [col for col in numeric_cols 
                     if not self.data[col].isna().all()]
        
        if not valid_cols:
            return {'message': 'No valid numeric columns for correlation analysis'}
        
        correlation_matrix = self.data[valid_cols].corr()
        # Replace NaN values with None for better readability
        correlation_dict = correlation_matrix.where(~correlation_matrix.isna(), None).to_dict()
        return correlation_dict