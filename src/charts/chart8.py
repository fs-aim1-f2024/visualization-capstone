from nicegui import ui
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

def create_chart8(app_state, **kwargs):
    """Danceability vs. Valence Scatter Plot with ML (Linear Regression)"""
    ui.label('Danceability vs. Valence Scatter Plot').classes('text-h6 hidden')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        # Ensure 'danceability_%' and 'valence_%' are numeric
        app_state.filtered_data['danceability_%'] = pd.to_numeric(app_state.filtered_data['danceability_%'], errors='coerce')
        app_state.filtered_data['valence_%'] = pd.to_numeric(app_state.filtered_data['valence_%'], errors='coerce')
        
        # Drop rows with missing values in either column
        data = app_state.filtered_data.dropna(subset=['danceability_%', 'valence_%'])
        
        # ML Technique: Fit a linear regression model to quantify the relationship
        X = data[['danceability_%']]
        y = data['valence_%']
        reg_model = LinearRegression()
        reg_model.fit(X, y)
        
        # Generate predictions for the regression line
        data['predicted_valence'] = reg_model.predict(X)
        
        # Sort data by danceability_% for a smooth regression line plot
        data_sorted = data.sort_values('danceability_%')
        
        # Create the scatter plot using Plotly Express
        fig = px.scatter(
            data,
            x='danceability_%',
            y='valence_%',
            labels={'danceability_%': 'Danceability (%)', 'valence_%': 'Valence (%)'},
            # title='Danceability vs. Valence Scatter Plot'
        )
        
        # Add the regression line to the chart
        fig.add_scatter(
            x=data_sorted['danceability_%'],
            y=data_sorted['predicted_valence'],
            mode='lines',
            name='Trend Line',
            line=dict(color='red')
        )
        
        # Display the chart in the UI
        with ui.row().classes('w-full'):
            ui.plotly(fig).classes('w-full')
    
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
