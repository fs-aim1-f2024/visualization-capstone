from nicegui import ui

def create_chart2(app_state, **kwargs):
    """Relationship between Released Year and Streams"""
    ui.label('Relationship between Released Year and Streams').classes('text-h6 hidden')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        ui.label('Chart 2 - Coming Soon').classes('text-h4 text-grey-6')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
