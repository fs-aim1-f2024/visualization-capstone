# main.py
from nicegui import ui, app
import pandas as pd
from pathlib import Path
import os
from collections import namedtuple

# Import chart modules
from charts.chart1 import create_chart1
from charts.chart2 import create_chart2
from charts.chart3 import create_chart3
from charts.chart4 import create_chart4
from charts.chart5 import create_chart5
from charts.chart6 import create_chart6
from charts.chart7 import create_chart7
from charts.chart8 import create_chart8

Chart = namedtuple('Chart', ['name', 'requirements'])

charts = [
    Chart(name='Distribution of Released Year', requirements=['Use ML algorithms to analyse the distribution of released years for tracks on Spotify', 'Visualize the distribution using a histogram to show the frequency of tracks released in different years']),
    Chart(name='Relationship between Released Year and Streams', requirements=['Perform predictive analysis to understand the relationship between the released year and the number of streams using ML regression techniques.', 'Develop a predictive model to estimate the number of streams based on the released year', 'Create a scatter plot visualization to depict the relationship between released year and streams']),
    Chart(name='Distribution of Streams by Playlist Presence', requirements=['Aggregate streams by the presence of tracks in Spotify playlists (in_spotify_playlists) using ML techniques', 'Visualize the distribution using a stacked bar chart, where each bar represents playlist presence and the stacked segments represent the proportion of streams from each category']),
    Chart(name='Streams Trend Over Time', requirements=['Analyse the trend of streams over time using ML time series analysis techniques','Visualize the trend using a line chart, where the x-axis represents time (e.g., months or years) and the y-axis represents the number of streams']),
    Chart(name='Correlation Matrix Heatmap', requirements=['Generate a correlation matrix using ML techniques to explore the relationships between different variables (released year, streams, BPM, danceability, valence, energy, etc.)', 'Visualize the correlation matrix using a heatmap, where each cell represents the correlation coefficient between two variables']),
    Chart(name='Distribution of Streams by Artist Count ', requirements=['Aggregate streams by the count of artists involved in each track (artist_count) using ML techniques','Visualize the distribution using a bar chart, where each bar represents the number of artists and the height represents the number of streams']),
    Chart(name='Distribution of Streams by Key', requirements=['Aggregate streams by musical key (key) using ML techniques', 'Visualize the distribution using a pie chart, where each slice represents a key and the size represents the proportion of streams']),
    Chart(name='Danceability vs. Valence Scatter Plot', requirements=['Analyse the relationship between danceability and valence using ML techniques', 'Create a scatter plot visualization to depict the relationship between danceability and valence, where each point represents a track']),
]

# Initialize app state
class AppState:
    def __init__(self):
        self.data = None
        self.filtered_data = None
        self.current_filters = {}
    
    def load_data(self, filepath):
        """Load data from CSV file"""
        try:
            self.data = pd.read_csv(filepath, encoding='latin1')
            self.filtered_data = self.data.copy()
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def apply_filters(self, filters):
        """Apply filters to the data"""
        self.current_filters = filters
        self.filtered_data = self.data.copy()
        
        for column, value in filters.items():
            print(f"Applying filter to {column} with value {value}")
            if value:
                if isinstance(value, list):
                    self.filtered_data = self.filtered_data[self.filtered_data[column].isin(list(map(lambda x: x['value'], value)))]
                else:
                    self.filtered_data = self.filtered_data[self.filtered_data[column] == value]
        
        return self.filtered_data

# Create app state
app_state = AppState()

# Dashboard layout
@ui.page('/')
def dashboard():
    with ui.header().classes('bg-blue-800 text-white'):
        ui.label('Spotify Data Dashboard').classes('text-h4')
    
    def load_sample_data():
        """Load sample data for demonstration"""
        sample_path = Path('data/spotify-2023.csv')
        if sample_path.exists():
            success = app_state.load_data(sample_path)
            if success:
                ui.notify('Sample data loaded successfully!', type='positive')
                setup_filters()  # Setup filters after loading data
                update_dashboard()
            else:
                ui.notify('Failed to load sample data', type='negative')
        else:
            ui.notify('Sample data file not found', type='negative')
    
    def update_dashboard():
        """Update all charts with current data"""
        if app_state.data is not None:
            # Update charts
            for i, chart_container in enumerate(chart_containers):
                with chart_container:
                    chart_container.clear()
                    chart_functions[i](app_state)
    
    def apply_filter(column, value):
        """Apply filter and update charts"""
        filters = app_state.current_filters.copy()
        filters[column] = value
        app_state.apply_filters(filters)
        update_dashboard()
    
    def reset_filters():
        """Reset all filters"""
        app_state.filtered_data = app_state.data.copy()
        app_state.current_filters = {}
        update_dashboard()
        ui.notify('Filters reset', type='info')
    
    def setup_filters():
        """Create filter controls based on loaded data"""
        # Clear existing filters
        filter_container.clear()
        
        with filter_container:
            with ui.row().classes('flex-wrap gap-4 p-4 bg-gray-100 rounded-lg'):
                # Categorical filters
                categorical_columns = app_state.data.select_dtypes(include=['object']).columns.tolist()[:3]
                for column in categorical_columns:
                    values = app_state.data[column].unique().tolist()
                    if len(values) < 10:
                        ui.label(f'{column}').classes('text-sm font-medium')
                        dropdown = ui.select(options=values, label=column, with_input=True, multiple=True).classes('w-48')
                        dropdown.on('update:model-value', lambda e, col=column: apply_filter(col, e.args))
                
                # Released Year filter
                year_values = sorted(app_state.data['released_year'].unique().tolist())
                year_select = ui.select(
                    options=[{i:i} for i in year_values],
                    label='Year',
                    with_input=True,
                    multiple=True
                ).classes('w-48')
                year_select.on('update:model-value', lambda e: apply_filter('released_year', e.args))
                
                # Artist Count filter')
                artist_count_values = sorted(app_state.data['artist_count'].unique().tolist())
                artist_count_select = ui.select(
                    options=[{i:i} for i in artist_count_values],
                    label='Artist Count',
                    with_input=True,
                    multiple=True
                ).classes('w-48')
                artist_count_select.on('update:model-value', lambda e: apply_filter('artist_count', e.args))
                
                # Released Month filter
                month_select = ui.select(
                    options=[{i:f'Month {i}'} for i in range(1, 13)],
                    label='Month',
                    with_input=True,
                    multiple=True
                ).classes('w-48')
                month_select.on('update:model-value', lambda e: apply_filter('released_month', e.args))
                
                # Released Day filter
                day_values = sorted(app_state.data['released_day'].unique().tolist())
                day_select = ui.select(
                    options=[{i:i} for i in day_values],
                    label='Day',
                    with_input=True,
                    multiple=True
                ).classes('w-48')
                day_select.on('update:model-value', lambda e: apply_filter('released_day', e.args))
                
                # Mode filter
                mode_select = ui.select(
                    options=[{0: 'Minor'}, {1: 'Major'}],
                    label='Mode',
                    with_input=True,
                    multiple=True
                ).classes('w-48')
                mode_select.on('update:model-value', lambda e: apply_filter('mode', e.args))
    
    def show_chart_dialog(chart_index):
        """Show a dialog with the full-size chart"""
        with ui.dialog() as dialog, ui.card().classes('w-[90vw] h-[90vh]'):
            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label(charts[chart_index].name).classes('text-h6')
                ui.button(icon='close', on_click=dialog.close).classes('bg-red-500 text-white hover:bg-red-600')
            with ui.element('div').classes('w-full h-[calc(90vh-4rem)]'):
                chart_functions[chart_index](app_state)
        dialog.open()

    # Create a list of chart functions
    chart_functions = [create_chart1, create_chart2, create_chart3, create_chart4, 
                      create_chart5, create_chart6, create_chart7, create_chart8]
    
    # Create the main layout
    with ui.column().classes('w-full p-4'):
            # ui.label('Data Loading and Preprocessing').classes('text-h6 mb-4')
            # with ui.row():
            #     ui.button('Load Sample Data', on_click=lambda: load_sample_data())
        with ui.card().classes('w-full mt-4'):
            ui.label('Data Filters').classes('text-h6 mb-2')
            filter_container = ui.element('div').classes('w-full')
            filter_container.clear()
            ui.button('Reset Filters', on_click=reset_filters).classes('mt-2')
        
        # Create a grid of charts
        chart_containers = []
        with ui.grid().classes('w-full gap-4 grid-cols-2'):
            for i in range(len(charts)):
                with ui.card().classes('w-full cursor-pointer hover:shadow-lg transition-shadow relative') as container:
                    # Add fullscreen button in top right
                    with ui.button(icon='fullscreen', on_click=lambda e, idx=i: show_chart_dialog(idx)).classes('absolute top-2 right-2 z-10 bg-white rounded-full shadow-md hover:bg-gray-100'):
                        ui.tooltip('Open in fullscreen')
                    
                    container.on('click', lambda e, idx=i: show_chart_dialog(idx))
                    ui.label(charts[i].name).classes('text-h6 mb-2')
                    chart_containers.append(container)
                    # Initial empty state
                    ui.label('Click to load chart').classes('text-grey-6')

  
    # Load data automatically when page starts
    load_sample_data()


# Run the app
ui.run(title='Spotify Data Dashboard')