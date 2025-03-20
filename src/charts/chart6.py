from nicegui import ui
import plotly.express as px
import numpy as np

def create_chart6(app_state):
    """Correlation heatmap of audio features"""
    ui.label('Audio Features Correlation').classes('text-h6')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        features = ['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 'instrumentalness_%']
        corr_matrix = app_state.filtered_data[features].corr().round(2)
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale='RdBu_r',
            title='Audio Features Correlation Matrix'
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        
        ui.plotly(fig).classes('w-full h-64')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')