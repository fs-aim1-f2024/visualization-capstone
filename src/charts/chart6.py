from nicegui import ui
import pandas as pd
import plotly.express as px

def create_chart6(app_state, **kwargs):
    """Distribution of Streams by Artist Count (Bar Chart)"""
    ui.label('Distribution of Streams by Artist Count').classes('text-h6 hidden')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        # Ensure 'streams' and 'artist_count' are numeric
        app_state.filtered_data['streams'] = pd.to_numeric(app_state.filtered_data['streams'], errors='coerce')
        app_state.filtered_data['artist_count'] = pd.to_numeric(app_state.filtered_data['artist_count'], errors='coerce')
        
        # Drop rows with missing or invalid values in either column
        data = app_state.filtered_data.dropna(subset=['streams', 'artist_count'])
        
        # Aggregate the total streams for each artist_count value
        agg_data = data.groupby('artist_count')['streams'].sum().reset_index()
        
        # Create the bar chart using Plotly Express
        fig = px.bar(
            agg_data,
            x='artist_count',
            y='streams',
            labels={'artist_count': 'Number of Artists', 'streams': 'Total Streams'},
            # title='Distribution of Streams by Artist Count'
        )
        
        # Update the chart layout 
        fig.update_layout(
            xaxis_title='Artist Count',
            yaxis_title='Total Streams'
        )
        
        # Display the chart in the UI
        with ui.row().classes('w-full'):
            ui.plotly(fig).classes('w-full')
    
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
