from nicegui import ui

def create_chart6(app_state):
    """Distribution of Streams by Artist Count"""
    ui.label('Distribution of Streams by Artist Count').classes('text-h6')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        ui.label('Chart 6 - Coming Soon').classes('text-h4 text-grey-6')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')