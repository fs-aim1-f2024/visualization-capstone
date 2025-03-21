from nicegui import ui

def create_chart4(app_state):
    """Streams Trend Over Time"""
    ui.label('Streams Trend Over Time').classes('text-h6')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        ui.label('Chart 4 - Coming Soon').classes('text-h4 text-grey-6')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')