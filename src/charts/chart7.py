from nicegui import ui
import pandas as pd
import plotly.express as px

def create_chart7(app_state, **kwargs):
    """Distribution of Streams by Musical Key (Pie Chart)"""
    ui.label('Distribution of Streams by Musical Key').classes('text-h6 hidden')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        # Ensure 'streams' and 'key' columns are numeric/strings as needed
        app_state.filtered_data['streams'] = pd.to_numeric(app_state.filtered_data['streams'], errors='coerce')
        app_state.filtered_data['key'] = app_state.filtered_data['key'].astype(str)
        
        # Drop rows with missing values in 'streams' or 'key'
        data = app_state.filtered_data.dropna(subset=['streams', 'key'])
        
        # Aggregate streams by musical key
        agg_data = data.groupby('key')['streams'].sum().reset_index()
        
        # Create the pie chart using Plotly Express
        fig = px.pie(
            agg_data,
            names='key',
            values='streams',
            # title='Distribution of Streams by Musical Key',
            color_discrete_sequence=px.colors.qualitative.Set1,
            hole=0  # Use hole=0 for a regular pie chart (set >0 for donut chart)
        )
        
        # Display the chart in the UI
        with ui.row().classes('w-full'):
            ui.plotly(fig).classes('w-full')
            
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
