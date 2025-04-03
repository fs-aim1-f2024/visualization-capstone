from nicegui import ui
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def create_chart5(app_state, **kwargs):
    """Correlation Matrix Heatmap with Values Inside the Boxes"""
    ui.label('Correlation Matrix Heatmap').classes('text-h6 hidden')

    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return

    try:
        # Select numeric columns
        numeric_columns = [
            'released_year', 'streams', 'bpm', 'danceability_%', 
            'valence_%', 'energy_%', 'acousticness_%', 
            'instrumentalness_%', 'liveness_%', 'speechiness_%'
        ]

        # Ensure numeric columns are converted properly
        for col in numeric_columns:
            app_state.filtered_data[col] = pd.to_numeric(app_state.filtered_data[col], errors='coerce')

        # Drop rows with missing values
        clean_data = app_state.filtered_data[numeric_columns].dropna()

        # Generate correlation matrix
        correlation_matrix = clean_data.corr(method='pearson')

        # Mask upper triangle to avoid duplication
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))

        # Create heatmap with custom colorscale (from white to blue)
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale=[[0, '#E0F7FA'], [1, '#388E3C']],  # Custom colorscale
            colorbar=dict(title='Correlation'),
            showscale=True,
            zmin=0,  # Minimum value is 0
            zmax=1,  # Maximum value is 1
        ))

        # Add values in cells
        for i in range(len(correlation_matrix.columns)):
            for j in range(len(correlation_matrix.columns)):
                fig.add_annotation(
                    x=correlation_matrix.columns[j],
                    y=correlation_matrix.columns[i],
                    text=f"{correlation_matrix.iloc[i, j]:.2f}",
                    showarrow=False,
                    font=dict(size=12, color='black'),
                    align='center',
                    valign='middle'
                )

        # Update layout
        fig.update_layout(
            xaxis_title='Features',
            yaxis_title='Features',
            xaxis=dict(showgrid=False, tickangle=45),
            yaxis=dict(showgrid=False),
            margin=dict(l=40, r=40, t=40, b=40),
            autosize=True
        )

        with ui.row().classes('w-full'):
            ui.plotly(fig).classes('w-full')

    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
