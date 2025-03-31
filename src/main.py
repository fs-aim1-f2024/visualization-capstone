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
    Chart(name='Distribution of Released Year', 
          requirements=['Use ML algorithms to analyse the distribution of released years for tracks on Spotify', 
                        'Visualize the distribution using a histogram to show the frequency of tracks released in different years']),
    Chart(name='Relationship between Released Year and Streams', 
          requirements=['Perform predictive analysis to understand the relationship between the released year and the number of streams using ML regression techniques.', 
                        'Develop a predictive model to estimate the number of streams based on the released year', 'Create a scatter plot visualization to depict the relationship between released year and streams']),
    Chart(name='Distribution of Streams by Playlist Presence', 
          requirements=['Aggregate streams by the presence of tracks in Spotify playlists (in_spotify_playlists) using ML techniques', 
                        'Visualize the distribution using a stacked bar chart, where each bar represents playlist presence and the stacked segments represent the proportion of streams from each category']),
    Chart(name='Streams Trend Over Time', 
          requirements=['Analyse the trend of streams over time using ML time series analysis techniques',
                        'Visualize the trend using a line chart, where the x-axis represents time (e.g., months or years) and the y-axis represents the number of streams']),
    Chart(name='Correlation Matrix Heatmap', 
          requirements=['Generate a correlation matrix using ML techniques to explore the relationships between different variables (released year, streams, BPM, danceability, valence, energy, etc.)', 
                        'Visualize the correlation matrix using a heatmap, where each cell represents the correlation coefficient between two variables']),
    Chart(name='Distribution of Streams by Artist Count ', 
          requirements=['Aggregate streams by the count of artists involved in each track (artist_count) using ML techniques',
                        'Visualize the distribution using a bar chart, where each bar represents the number of artists and the height represents the number of streams']),
    Chart(name='Distribution of Streams by Key', 
          requirements=['Aggregate streams by musical key (key) using ML techniques', 
                        'Visualize the distribution using a pie chart, where each slice represents a key and the size represents the proportion of streams']),
    Chart(name='Danceability vs. Valence Scatter Plot', 
          requirements=['Analyse the relationship between danceability and valence using ML techniques', 
                        'Create a scatter plot visualization to depict the relationship between danceability and valence, where each point represents a track']),
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
            self.preprocess_data()
            self.filtered_data = self.data.copy()
            return True
        except Exception as e:
            ui.notify(f"Error loading data: {e}", type='negative')
            return False
    
    def preprocess_data(self):  
        # Select numeric columns
        numeric_columns = [
            'artist_count', 'released_year','released_month', 'released_day', 'streams', 'bpm', 'danceability_%', 
            'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%', 'liveness_%', 'speechiness_%',
            'in_spotify_playlists', 'in_spotify_charts', 'in_apple_playlists','in_apple_charts',
            'in_deezer_playlists', 'in_deezer_charts', 'in_shazam_charts', 'bpm',
        ]

        # Ensure numeric columns are converted properly
        for col in numeric_columns:
            self.data[col] = pd.to_numeric(self.data[col], errors='coerce')
 
        # Avoid chained assignment
        self.data.loc[:, 'released_year'].fillna(2000, inplace=True)
        self.data.loc[:, 'released_month'].fillna(1, inplace=True)
        self.data.loc[:, 'released_day'].fillna(1, inplace=True)

        # Clip date values within valid ranges
        self.data.loc[:, 'released_month'] = self.data['released_month'].clip(1, 12).astype(int)
        self.data.loc[:, 'released_day'] = self.data['released_day'].clip(1, 31).astype(int)

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
    
    def apply_filter(column, value, submit=False):
        """Apply filter and update charts"""
        filters = app_state.current_filters.copy()  
        if column is not None:
            filters[column] = value 
            app_state.apply_filters(filters) 
        if submit:
            create_chart_panels.refresh()
            ui.notify('Filter applied', type='info')
    
    def reset_filters():
        """Reset all filters"""
        app_state.filtered_data = app_state.data.copy()
        app_state.current_filters = {}
        setup_filters()
        create_chart_panels.refresh()
        ui.notify('Filters reset', type='info')
    
    def popup_data():
        """Show a dialog with the data"""
        with ui.dialog().props('full-width full-height') as dialog, ui.card():
            ui.label('Data').classes('text-h6')
            ui.aggrid.from_pandas(app_state.data, auto_size_columns=False).classes('w-full h-full')
        dialog.open()
    
    # Set the colors for the app with Spotify theme
    ui.colors(primary="#1DB954", secondary="#191414", accent="#FFFFFF", positive="#1ED760", negative="#FF5722")
    
    with ui.header().classes('bg-gradient-to-tr from-green-600 to-green-400') as header:
        with ui.card().classes('w-full items-center transition-all duration-300 header-collapsed').style('display: none'):
            with ui.row().classes('w-full justify-between items-center'):
                with ui.row():
                    ui.html('<svg xmlns="http://www.w3.org/2000/svg" height="30" viewBox="-33.4974 -55.829 290.3108 334.974"><path d="M177.707 98.987c-35.992-21.375-95.36-23.34-129.719-12.912-5.519 1.674-11.353-1.44-13.024-6.958-1.672-5.521 1.439-11.352 6.96-13.029 39.443-11.972 105.008-9.66 146.443 14.936 4.964 2.947 6.59 9.356 3.649 14.31-2.944 4.963-9.359 6.6-14.31 3.653m-1.178 31.658c-2.525 4.098-7.883 5.383-11.975 2.867-30.005-18.444-75.762-23.788-111.262-13.012-4.603 1.39-9.466-1.204-10.864-5.8a8.717 8.717 0 015.805-10.856c40.553-12.307 90.968-6.347 125.432 14.833 4.092 2.52 5.38 7.88 2.864 11.968m-13.663 30.404a6.954 6.954 0 01-9.569 2.316c-26.22-16.025-59.223-19.644-98.09-10.766a6.955 6.955 0 01-8.331-5.232 6.95 6.95 0 015.233-8.334c42.533-9.722 79.017-5.538 108.448 12.446a6.96 6.96 0 012.31 9.57M111.656 0C49.992 0 0 49.99 0 111.656c0 61.672 49.992 111.66 111.657 111.66 61.668 0 111.659-49.988 111.659-111.66C223.316 49.991 173.326 0 111.657 0" fill="#000000"/></svg>')
                    ui.label('Spotify Data Dashboard').classes('text-dark text-h6') 
            
        with ui.card().classes('w-full items-center transition-all duration-300 header-expanded'):
            with ui.row().classes('w-full justify-between items-center'):
                with ui.row():
                    ui.html('<svg xmlns="http://www.w3.org/2000/svg" height="30" viewBox="-33.4974 -55.829 290.3108 334.974"><path d="M177.707 98.987c-35.992-21.375-95.36-23.34-129.719-12.912-5.519 1.674-11.353-1.44-13.024-6.958-1.672-5.521 1.439-11.352 6.96-13.029 39.443-11.972 105.008-9.66 146.443 14.936 4.964 2.947 6.59 9.356 3.649 14.31-2.944 4.963-9.359 6.6-14.31 3.653m-1.178 31.658c-2.525 4.098-7.883 5.383-11.975 2.867-30.005-18.444-75.762-23.788-111.262-13.012-4.603 1.39-9.466-1.204-10.864-5.8a8.717 8.717 0 015.805-10.856c40.553-12.307 90.968-6.347 125.432 14.833 4.092 2.52 5.38 7.88 2.864 11.968m-13.663 30.404a6.954 6.954 0 01-9.569 2.316c-26.22-16.025-59.223-19.644-98.09-10.766a6.955 6.955 0 01-8.331-5.232 6.95 6.95 0 015.233-8.334c42.533-9.722 79.017-5.538 108.448 12.446a6.96 6.96 0 012.31 9.57M111.656 0C49.992 0 0 49.99 0 111.656c0 61.672 49.992 111.66 111.657 111.66 61.668 0 111.659-49.988 111.659-111.66C223.316 49.991 173.326 0 111.657 0" fill="#000000"/></svg>')
                    ui.label('Spotify Data Dashboard').classes('text-dark text-h6')
                with ui.row():
                    ui.button(icon='list', text='View Data', on_click=popup_data).classes('p-1').props('flat')
                    ui.button(icon='refresh', text='Reset Filters', on_click=reset_filters).classes('p-1').props('flat')
            filter_container = ui.element('div').classes('w-full')
            filter_container.clear()
            
    # Set initial state
    header.expanded = True
    header.collapsed = False
    
    def load_sample_data():
        """Load sample data for demonstration"""
        sample_path = Path('data/spotify-2023.csv')
        if sample_path.exists():
            success = app_state.load_data(sample_path)
            if success:
                ui.notify('Sample data loaded successfully!', type='positive')
                setup_filters()  # Setup filters after loading data
                create_chart_panels.refresh()
            else:
                ui.notify('Failed to load sample data', type='negative')
        else:
            ui.notify('Sample data file not found', type='negative')
     
    
    def setup_filters():
        """Create filter controls based on loaded data"""
        # Clear existing filters
        filter_container.clear()
        
        with filter_container:
            with ui.grid().classes('grid-cols-1 md:grid-cols-3 lg:grid-cols-6'):
                # Released Year filter
                year_values = sorted(app_state.data['released_year'].unique().tolist())
                year_select = ui.select(
                    options=dict(zip(year_values, year_values)),
                    label='Year',
                    with_input=True,
                    multiple=True,
                    on_change=lambda e: apply_filter('released_year', e.value)
                ).classes('w-full').props("outlined dense")
                
                # Released Month filter
                month_select = ui.select(
                    options=dict(zip(range(1, 13), [f'Month {i}' for i in range(1, 13)])),
                    label='Month',
                    with_input=True,
                    multiple=True,
                    on_change=lambda e: apply_filter('released_month', e.value)
                ).classes('w-full').props("outlined dense")
                
                # Released Day filter
                day_values = sorted(app_state.data['released_day'].unique().tolist())
                day_select = ui.select(
                    options=dict(zip(day_values, day_values)),
                    label='Day',
                    with_input=True,
                    multiple=True,
                    on_change=lambda e: apply_filter('released_day', e.value)
                ).classes('w-full').props("outlined dense")
                
                # Artist Count filter')
                artist_count_values = sorted(app_state.data['artist_count'].unique().tolist())
                artist_count_select = ui.select(
                    options=dict(zip(artist_count_values, artist_count_values)),
                    label='Artist Count',
                    with_input=True,
                    multiple=True,
                    on_change=lambda e: apply_filter('artist_count', e.value)
                ).classes('w-full').props("outlined dense")
                
                # Mode filter
                mode_select = ui.select(
                    options=dict(zip(['Minor', 'Major'], ['Minor', 'Major'])),
                    label='Mode',
                    with_input=True,
                    multiple=True,
                    on_change=lambda e: apply_filter('mode', e.value)
                ).classes('w-full').props("outlined dense")
                
                with ui.column().classes('justify-end'):
                    ui.button('Apply Filters', icon='filter_list').on_click(lambda: apply_filter(None, None, True))
    
    def show_chart_info(chart_index):
        """Show a dialog with the chart information"""
        with ui.dialog() as dialog, ui.card():
            ui.label(charts[chart_index].name).classes('text-h6')
            for requirement in charts[chart_index].requirements:
                ui.label(requirement).classes('text-sm')
        dialog.open()
    
    def show_chart_dialog(chart_index):
        """Show a dialog with the full-size chart"""
        with ui.dialog().props('full-width full-height') as dialog, ui.card():
            with ui.row().classes('w-full justify-between items-start'):
                ui.label(charts[chart_index].name).classes('text-h6')
                ui.button(icon='close', on_click=dialog.close).props('flat')
            with ui.element('div').classes('w-full h-full flex items-center justify-center'):
                chart_functions[chart_index](app_state, is_full_screen=True, requirements=charts[chart_index].requirements)
        dialog.open()
        
    @ui.refreshable
    def create_chart_panels():
        chart_containers = []
        #Create the main layout
        with ui.column().classes('w-full'):      
            with ui.grid().classes('w-full gap-4 grid-cols-1 lg:grid-cols-2'):
                for i in range(len(charts)):
                    with ui.card().classes('w-full cursor-pointer hover:shadow-lg transition-shadow relative') as container:
                        ui.label(charts[i].name).classes('text-h6')
                        chart_containers.append(container)
                        
        for i, chart_container in enumerate(chart_containers):
            with chart_container:
                chart_container.clear()
                # Add fullscreen button in top right
                with ui.row():
                    ui.label(charts[i].name).classes('text-h6')
                    with ui.button(icon='info', on_click=lambda e, idx=i: show_chart_info(idx)).classes('absolute top-2 right-12 z-10').props('flat'):
                        ui.tooltip('Show requirements')
                    with ui.button(icon='fullscreen', on_click=lambda e, idx=i: show_chart_dialog(idx)).classes('absolute top-2 right-2 z-10').props('flat'):
                        ui.tooltip('Open in fullscreen')
                
                chart_functions[i](app_state)
                
    # Create a list of chart functions
    chart_functions = [create_chart1, create_chart2, create_chart3, create_chart4, 
                      create_chart5, create_chart6, create_chart7, create_chart8]
    
    # Create the main layout
    create_chart_panels()
    
    # Load data automatically when page starts 
    load_sample_data()  
    
 # Add JavaScript to handle scroll behavior
        # Create JavaScript functions to handle state
    ui.add_body_html('''
    <script>
    window.updateHeaderState = function(isCollapsed) {
        // This function will be called from Python
        const expandedElements = document.querySelectorAll('.header-expanded');
        const collapsedElements = document.querySelectorAll('.header-collapsed');
        
        if (isCollapsed) {
            expandedElements.forEach(el => el.style.display = 'none');
            collapsedElements.forEach(el => el.style.display = 'flex');
        } else {
            expandedElements.forEach(el => el.style.display = 'flex');
            collapsedElements.forEach(el => el.style.display = 'none');
        }
    }
    </script>
    ''')
    
    # Add JavaScript to handle scroll behavior
    ui.add_body_html('''
    <script>
    let lastScrollTop = 0;
    
    document.addEventListener('scroll', function() {
        const header = document.querySelector('.q-header');
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Determine scroll direction
        const scrollingDown = scrollTop > lastScrollTop;
        lastScrollTop = scrollTop;
        
        // Get the header height based on scroll position and direction
        if (scrollTop > 10) {
            window.updateHeaderState(true);
        } else {
            window.updateHeaderState(false);
        }
    });
    </script>
    ''') 

if __name__ in {"__main__", "__mp_main__"}: 

# Run the app   
    ui.run(title='Spotify Data Dashboard', host='0.0.0.0', port=8080) 