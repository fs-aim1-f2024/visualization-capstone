from nicegui import ui
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_chart8(app_state):
    """Line plot of streams by release date"""
    ui.label('Streams by Release Date').classes('text-h6')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        # Convert released_year to datetime and aggregate streams
        chart_data = (app_state.filtered_data.groupby('released_year')['streams']
                     .mean()
                     .reset_index())
        
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=chart_data['released_year'],
                y=chart_data['streams'],
                mode='lines+markers',
                name='Average Streams'
            )
        )
        
        fig.update_layout(
            title='Average Streams by Release Year',
            xaxis_title='Release Year',
            yaxis_title='Average Streams',
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        ui.plotly(fig).classes('w-full h-64')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')