import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

class Dashboard:
    def __init__(self, data):
        self.data = data
        self.colors = {
            'primary': '#636EFA',
            'secondary': '#EF553B',
            'background': '#FFFFFF',
            'text': '#000000'
        }

    def create_age_distribution_plot(self):
        """Create age distribution visualization"""
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=self.data['age'],
            nbinsx=20,
            name='Age Distribution',
            marker_color=self.colors['primary']
        ))

        fig.update_layout(
            title='User Age Distribution',
            xaxis_title='Age',
            yaxis_title='Number of Users',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background']
        )
        
        return fig

    def create_location_map(self):
        """Create geographical distribution map"""
        location_counts = self.data['location'].value_counts().reset_index()
        location_counts.columns = ['location', 'count']

        fig = px.choropleth(
            location_counts,
            locations='location',
            locationmode='country names',
            color='count',
            title='User Geographic Distribution',
            color_continuous_scale='Viridis'
        )

        fig.update_layout(
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background'],
            geo=dict(showframe=False)
        )
        
        return fig

    def create_registration_timeline(self):
        """Create registration timeline visualization"""
        daily_registrations = self.data.groupby('created_at').size().reset_index(name='count')
        daily_registrations = daily_registrations.sort_values('created_at')
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_registrations['created_at'],
            y=daily_registrations['count'].cumsum(),
            mode='lines',
            name='Cumulative Registrations',
            line=dict(color=self.colors['primary'])
        ))

        fig.update_layout(
            title='User Registration Timeline',
            xaxis_title='Date',
            yaxis_title='Number of Users',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background']
        )
        
        return fig

    def create_age_location_plot(self):
        """Create age by location box plot"""
        fig = go.Figure()

        fig.add_trace(go.Box(
            x=self.data['location'],
            y=self.data['age'],
            name='Age Distribution by Location',
            marker_color=self.colors['primary']
        ))

        fig.update_layout(
            title='Age Distribution by Location',
            xaxis_title='Location',
            yaxis_title='Age',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['background'],
            showlegend=False
        )

        return fig

    def create_dashboard(self):
        """Create complete dashboard with all visualizations"""
        # Create and save all plots
        age_dist = self.create_age_distribution_plot()
        loc_map = self.create_location_map()
        reg_timeline = self.create_registration_timeline()
        age_loc = self.create_age_location_plot()

        # Save plots as HTML files
        age_dist.write_html("web_app/static/plots/age_distribution.html")
        loc_map.write_html("web_app/static/plots/location_map.html")
        reg_timeline.write_html("web_app/static/plots/registration_timeline.html")
        age_loc.write_html("web_app/static/plots/age_location.html")

        return {
            'age_distribution': age_dist,
            'location_map': loc_map,
            'registration_timeline': reg_timeline,
            'age_location': age_loc
        }