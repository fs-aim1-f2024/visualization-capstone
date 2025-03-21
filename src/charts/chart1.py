from nicegui import ui
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KernelDensity

def create_chart1(app_state):
    """Histogram showing distribution of released years with KDE"""
    ui.label('Distribution of Released Years').classes('text-h6 hidden')
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        # Get released years data
        years = app_state.filtered_data['released_year'].values
        
        # Create histogram with KDE
        fig = go.Figure()
        
        # Add histogram
        fig.add_trace(go.Histogram(
            x=years,
            name='Histogram',
            nbinsx=30,
            histnorm='probability density',
            marker_color='#1f77b4'
        ))
        
        # Fit KDE
        kde = KernelDensity(bandwidth=1.0, kernel='gaussian')
        kde.fit(years.reshape(-1, 1))
        
        # Generate points for KDE curve
        x_grid = np.linspace(years.min(), years.max(), 100).reshape(-1, 1)
        log_dens = kde.score_samples(x_grid)
        dens = np.exp(log_dens)
        
        # Add KDE curve
        fig.add_trace(go.Scatter(
            x=x_grid.flatten(),
            y=dens,
            name='KDE',
            line=dict(color='#ff7f0e', width=2)
        ))
        
        # Update layout
        fig.update_layout(
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis_title='Release Year',
            yaxis_title='Probability Density',
            title='Distribution of Track Release Years',
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Add statistical information
        stats_text = f"""
        Statistics:
        Mean Year: {np.mean(years):.1f}
        Median Year: {np.median(years):.1f}
        Mode Year: {float(np.bincount(years.astype(int)).argmax())}
        Standard Deviation: {np.std(years):.1f}
        """
        
        with ui.row().classes('w-full'):
            ui.plotly(fig).classes('w-3/4 h-64')
            ui.label(stats_text).classes('w-1/4 text-sm')
            
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')