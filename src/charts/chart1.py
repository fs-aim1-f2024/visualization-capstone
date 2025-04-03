from nicegui import ui
import plotly.express as px

def create_chart1(app_state, **kwargs):
    """Distribution of Realeased year"""
    is_full_screen = kwargs.get('is_full_screen', False)
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        # Get released years data
        years = app_state.filtered_data['released_year'].values
        
        # Create histogram showing count of records by year
        fig = px.histogram(
            years, 
            nbins=30,  # Adjust bin count for better visualization
            labels={'x': 'Release Year', 'y': 'Count'},
            color_discrete_sequence=['#1DB954']  # Spotify green color
        )
        
        # Update layout for better readability
        fig.update_layout(
            showlegend=False,
            bargap=0.1,  # Add gap between bars
            xaxis_title_font=dict(size=14),
            yaxis_title_font=dict(size=14),
            yaxis_title='Number of Tracks',
            xaxis_title='Released Year'
        )

        with ui.row().classes('w-full'):
            ui.plotly(fig).classes('w-full')
            
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')