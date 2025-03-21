from nicegui import ui

def create_chart3(app_state):
    """Distribution of Streams by Playlist Presence"""
    ui.label('Distribution of Streams by Playlist Presence').classes('text-h6')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        ui.label('Chart 3 - Coming Soon').classes('text-h4 text-grey-6')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
