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
            if value:
                if isinstance(value, list):
                    self.filtered_data = self.filtered_data[self.filtered_data[column].isin(value)]
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
    
    def load_uploaded_data(event):
        """Handle uploaded CSV file"""
        temp_path = Path(event.name)
        with open(temp_path, 'wb') as f:
            f.write(event.content.read())
        
        success = app_state.load_data(temp_path)
        if success:
            ui.notify('Data loaded successfully!', type='positive')
            setup_filters()  # Setup filters after loading data
            update_dashboard()
        else:
            ui.notify('Failed to load data', type='negative')
        
        # Clean up temporary file
        os.remove(temp_path)
    
    def update_dashboard():
        """Update all charts with current data"""
        if app_state.data is not None:
            # Update charts
            with chart1_container:
                chart1_container.clear()
                create_chart1(app_state)
            
            with chart2_container:
                chart2_container.clear()
                create_chart2(app_state)
                
            with chart3_container:
                chart3_container.clear()
                create_chart3(app_state)
                
            with chart4_container:
                chart4_container.clear()
                create_chart4(app_state)
                
            with chart5_container:
                chart5_container.clear()
                create_chart5(app_state)
                
            with chart6_container:
                chart6_container.clear()
                create_chart6(app_state)
                
            with chart7_container:
                chart7_container.clear()
                create_chart7(app_state)
                
            with chart8_container:
                chart8_container.clear()
                create_chart8(app_state)
    
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
            with ui.row():
                # Create filters for categorical columns (example)
                categorical_columns = app_state.data.select_dtypes(include=['object']).columns.tolist()[:3]  # Limit to first 3 categorical columns
                
                for column in categorical_columns:
                    values = app_state.data[column].unique().tolist()
                    if len(values) < 10:  # Only create dropdowns for columns with reasonable number of values
                        with ui.card().classes('p-2'):
                            ui.label(f'Filter by {column}')
                            dropdown = ui.select(options=values, label=column, with_input=True, multiple=True)
                            dropdown.on('update:model-value', lambda e, col=column: apply_filter(col, e.value))
    
    # Replace grid with tabs
    with ui.tabs().classes('w-full') as tabs:
        tab_preprocessing = ui.tab('Data Preprocessing')
        tab1 = ui.tab(charts[0].name)
        tab2 = ui.tab(charts[1].name)
        tab3 = ui.tab(charts[2].name)
        tab4 = ui.tab(charts[3].name)
        tab5 = ui.tab(charts[4].name)
        tab6 = ui.tab(charts[5].name)
        tab7 = ui.tab(charts[6].name)
        tab8 = ui.tab(charts[7].name)
    
    with ui.tab_panels(tabs, value=tab_preprocessing).classes('w-full'):
        with ui.tab_panel(tab_preprocessing):
            with ui.card().classes('w-full p-4'):
                ui.label('Data Loading and Preprocessing').classes('text-h6 mb-4')
                with ui.row():
                    ui.button('Load Sample Data', on_click=lambda: load_sample_data())
                    file_picker = ui.upload(on_upload=lambda e: load_uploaded_data(e))
                
                with ui.card().classes('w-full mt-4'):
                    ui.label('Data Filters').classes('text-h6 mb-2')
                    filter_container = ui.element('div').classes('w-full')
                    filter_container.clear()
                    
                    # Add a button to reset filters
                    ui.button('Reset Filters', on_click=reset_filters).classes('mt-2')
        
        with ui.tab_panel(tab1):
            chart1_container = ui.card().classes('w-full p-4')
        with ui.tab_panel(tab2):
            chart2_container = ui.card().classes('w-full p-4')
        with ui.tab_panel(tab3):
            chart3_container = ui.card().classes('w-full p-4')
        with ui.tab_panel(tab4):
            chart4_container = ui.card().classes('w-full p-4')
        with ui.tab_panel(tab5):
            chart5_container = ui.card().classes('w-full p-4')
        with ui.tab_panel(tab6):
            chart6_container = ui.card().classes('w-full p-4')
        with ui.tab_panel(tab7):
            chart7_container = ui.card().classes('w-full p-4')
        with ui.tab_panel(tab8):
            chart8_container = ui.card().classes('w-full p-4')

# Run the app
ui.run(title='Spotify Data Dashboard')