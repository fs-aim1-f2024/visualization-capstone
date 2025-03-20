from nicegui import ui
import plotly.express as px
import plotly.graph_objects as go

def create_chart1(app_state):
    """Bar chart showing top 10 artists by streams"""
    ui.label('Top 10 Artists by Streams').classes('text-h6')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        # Get top 10 artists by streams
        chart_data = (app_state.filtered_data.groupby('artist_s')['streams']
                     .sum()
                     .sort_values(ascending=False)
                     .head(10)
                     .reset_index())
        
        fig = px.bar(
            chart_data,
            x='artist_s',
            y='streams',
            title='Top 10 Artists by Total Streams'
        )
        
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis_title='Artist',
            yaxis_title='Total Streams'
        )
        
        ui.plotly(fig).classes('w-full h-64')
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')