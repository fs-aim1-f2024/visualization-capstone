from nicegui import ui
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

def create_chart2(app_state, **kwargs):
    """Relationship between Released Year and Streams"""
    ui.label('Relationship between Released Year and Streams').classes('text-h6 hidden')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
      
    try:
        
        # Prepare data for prediction
        X = pd.DataFrame(app_state.filtered_data['released_year'], columns=['released_year'])
        y = pd.DataFrame(app_state.filtered_data['streams'])

        # Train a linear regression model
        model = LinearRegression()
        model.fit(X, y)

        # Get the current maximum year from the data
        max_year = app_state.filtered_data['released_year'].max()

        # Create prediction line for visualization
        years_min = app_state.filtered_data['released_year'].min()
        years_max = app_state.filtered_data['released_year'].max() + 5
        years_range = np.linspace(years_min, years_max, 100)
        years_df = pd.DataFrame(years_range, columns=['released_year'])
        streams_pred = model.predict(years_df)
        # Create scatter plot of actual data
        fig = px.scatter(app_state.filtered_data, x='released_year', y='streams', 
                        labels={'released_year': 'Release Year', 'streams': 'Number of Streams'})

        # Add shaded area for prediction region
        fig.add_vrect(
            x0=max_year, x1=max_year + 5,
            fillcolor="rgba(255, 0, 0, 0.1)", opacity=0.5,
            layer="below", line_width=0,
            annotation_text="Prediction Area",
            annotation_position="top right",
        )
        
        # Add prediction line
        fig.add_trace(
            go.Scatter(
                x=years_range.flatten(), 
                y=streams_pred.flatten(),
                mode='lines',
                name='Prediction',
                line=dict(color='red', width=2)
            )
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title='Release Year',
            yaxis_title='Number of Streams',
            legend_title='Data',
        )
        
        with ui.row().classes('w-full'):
            ui.plotly(fig).classes('w-full') 
        
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
