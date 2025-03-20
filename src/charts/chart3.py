from nicegui import ui
import plotly.express as px

def create_chart3(app_state):
    """Box plot of streams by mode"""
    ui.label('Streams Distribution by Mode').classes('text-h6')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        fig = px.box(
            app_state.filtered_data,
            x='mode',
            y='streams',
            title='Distribution of Streams by Mode (Major/Minor)'
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        ui.plotly(fig).classes('w-full h-64')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
