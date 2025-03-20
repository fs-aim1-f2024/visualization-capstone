from nicegui import ui
import plotly.express as px

def create_chart5(app_state):
    """Box plot of valence by playlist_genre"""
    ui.label('Valence by Genre').classes('text-h6')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        fig = px.box(
            app_state.filtered_data,
            x='playlist_genre',
            y='valence_%',
            title='Valence Distribution by Genre'
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        ui.plotly(fig).classes('w-full h-64')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
