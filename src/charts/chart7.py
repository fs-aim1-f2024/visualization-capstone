from nicegui import ui
import plotly.express as px

def create_chart7(app_state):
    """Histogram of song tempos"""
    ui.label('Distribution of Tempo').classes('text-h6')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        fig = px.histogram(
            app_state.filtered_data,
            x='bpm',
            nbins=30,
            title='Distribution of Song Tempos (BPM)'
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        ui.plotly(fig).classes('w-full h-64')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')