from nicegui import ui

def create_chart5(app_state):
    """Correlation Matrix Heatmap"""
    ui.label('Correlation Matrix Heatmap').classes('text-h6 hidden')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        ui.label('Chart 5 - Coming Soon').classes('text-h4 text-grey-6')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
