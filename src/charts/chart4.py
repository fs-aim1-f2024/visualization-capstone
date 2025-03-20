from nicegui import ui
import plotly.express as px

def create_chart4(app_state):
    """Pie chart of key distribution"""
    ui.label('Distribution of Song Keys').classes('text-h6')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        key_counts = app_state.filtered_data['key'].value_counts()
        
        fig = px.pie(
            values=key_counts.values,
            names=key_counts.index,
            title='Distribution of Song Keys'
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        ui.plotly(fig).classes('w-full h-64')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')