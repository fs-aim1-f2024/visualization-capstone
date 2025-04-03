from nicegui import ui
import pandas as pd
import plotly.express as px

def create_chart3(app_state, **kwargs):
    """Distribution of Streams by Playlist Presence (Stacked)"""
    ui.label('Distribution of Streams by Playlist Presence (Stacked)').classes('text-h6 hidden')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        # Ensure columns are numeric
        app_state.filtered_data['streams'] = pd.to_numeric(app_state.filtered_data['streams'], errors='coerce')
        app_state.filtered_data['in_spotify_playlists'] = pd.to_numeric(app_state.filtered_data['in_spotify_playlists'], errors='coerce')
        
        # Drop rows with missing or invalid data after conversion to numeric
        app_state.filtered_data = app_state.filtered_data.dropna(subset=['streams', 'in_spotify_playlists'])
        
        # Define the stream bins
        stream_bins = [0, 100000000, 500000000, 1000000000, 2000000000, 3000000000, 4000000000, 5000000000, float('inf')]
        stream_labels = ['0-100M', '100M-500M', '500M-1B', '1B-2B', '2B-3B', '3B-4B', '4B-5B', '5B+']

        # Define the playlist bins
        playlist_bins = [0, 100, 500, 1000, 5000, 10000, 50000, float('inf')]
        playlist_labels = [
            '0-99 playlists', 
            '100-499 playlists', 
            '500-999 playlists', 
            '1000-4999 playlists', 
            '5000-9999 playlists', 
            '10000-49999 playlists', 
            '50000+ playlists'
        ]
        
        # Categorize streams and playlists into ranges
        app_state.filtered_data['stream_range'] = pd.cut(app_state.filtered_data['streams'], bins=stream_bins, labels=stream_labels, right=False)
        app_state.filtered_data['playlist_range'] = pd.cut(app_state.filtered_data['in_spotify_playlists'], bins=playlist_bins, labels=playlist_labels, right=False)
        
        # Aggregate the streams by playlist and stream ranges
        aggregated_data = app_state.filtered_data.groupby(['playlist_range', 'stream_range'])['streams'].sum().reset_index()
        
        # Create the stacked bar chart
        fig = px.bar(
            aggregated_data, 
            x='playlist_range',  
            y='streams',  
            color='stream_range',  
            labels={'x': 'Playlist Presence Range', 'y': 'Total Streams'},
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        
        # Update the chart layout
        fig.update_layout(
            barmode='stack',  
            showlegend=True,   
            bargap=0.2,  
            xaxis_title_font=dict(size=14),
            yaxis_title_font=dict(size=14),
            xaxis_title='Playlist Presence Range',
            yaxis_title='Total Streams'
        )
        
        # Display the chart in the UI
        with ui.row().classes('w-full'):
            ui.plotly(fig).classes('w-full')

    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
