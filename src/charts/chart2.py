from nicegui import ui
import plotly.express as px

def create_chart2(app_state):
    """Scatter plot of danceability vs energy"""
    ui.label('Danceability vs Energy').classes('text-h6')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        fig = px.scatter(
            app_state.filtered_data,
            x='danceability_%',
            y='energy_%',
            color='streams',
            hover_data=['track_name'],
            title='Danceability vs Energy (Color: Streams)'
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        ui.plotly(fig).classes('w-full h-64')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
