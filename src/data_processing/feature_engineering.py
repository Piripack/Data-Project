import pandas as pd

class FeatureEngineer:
    def create_user_features(self, data):
        """Create additional features from user data"""
        if data is None:
            return None

        # Create a copy of the data
        enhanced_df = data.copy()

        # Add registration-based features
        enhanced_df['registration_month'] = enhanced_df['created_at'].dt.month
        enhanced_df['registration_year'] = enhanced_df['created_at'].dt.year
        enhanced_df['registration_day'] = enhanced_df['created_at'].dt.day
        enhanced_df['registration_dayofweek'] = enhanced_df['created_at'].dt.dayofweek

        # Add age-based features
        age_bins = [0, 20, 30, 40, 50, 60, 100]
        age_labels = ['<20', '20-30', '30-40', '40-50', '50-60', '60+']
        enhanced_df['age_group'] = pd.cut(enhanced_df['age'], bins=age_bins, labels=age_labels)

        # Add location-based features
        enhanced_df['continent'] = enhanced_df['location'].map({
            'United States': 'North America',
            'Canada': 'North America',
            'Brazil': 'South America',
            'United Kingdom': 'Europe',
            'France': 'Europe',
            'Germany': 'Europe',
            'India': 'Asia',
            'Japan': 'Asia',
            'Australia': 'Oceania'
        })

        return enhanced_df