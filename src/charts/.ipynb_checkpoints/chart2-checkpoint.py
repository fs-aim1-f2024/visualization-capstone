from nicegui import ui
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def create_chart2(app_state, **kwargs):
    """Relationship between Released Year and Streams"""
    ui.label('Relationship between Released Year and Streams').classes('text-h6 hidden')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
      
    try:
        # Prepare data for prediction
        # Extract features and target
        group_df  = app_state.filtered_data['released_year'].value_counts().reset_index()
        X = pd.DataFrame(group_df['released_year'])
        y = group_df['count']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a linear regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R² Score: {r2:.2f}")

        # Create prediction line for visualization
        years_range = np.linspace(group_df['released_year'].min(), group_df['released_year'].max() + 5, 100).reshape(-1, 1)
        streams_pred = model.predict(years_range)

        # Create scatter plot of actual data
        fig = px.scatter(group_df, x='released_year', y='count', 
                        labels={'released_year': 'Release Year', 'count': 'Number of Streams'})

        # Add prediction line
        fig.add_trace(
            go.Scatter(
                x=years_range.flatten(), 
                y=streams_pred,
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
        
        ui.plotly(fig)
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
