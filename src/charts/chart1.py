from nicegui import ui
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KernelDensity

def create_chart1(app_state, **kwargs):
    is_full_screen = kwargs.get('is_full_screen', False)
    
    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return
    
    try:
        # Get released years data
        years = app_state.filtered_data['released_year'].values
        
        # Create histogram showing count of records by year
        fig = px.histogram(
            years, 
            nbins=30,  # Adjust bin count for better visualization
            labels={'x': 'Release Year', 'y': 'Count'},
            color_discrete_sequence=['#1DB954']  # Spotify green color
        )
        
        # Update layout for better readability
        fig.update_layout(
            showlegend=False,
            bargap=0.1,  # Add gap between bars
            xaxis_title_font=dict(size=14),
            yaxis_title_font=dict(size=14),
            yaxis_title='Number of Tracks',
            xaxis_title='Release Year'
        )

        # # Create histogram with KDE
        # fig = go.Figure()
        
        # # Add histogram
        # fig.add_trace(go.Histogram(
        #     x=years,
        #     name='Histogram',
        #     nbinsx=30,
        #     histnorm='probability density',
        #     marker_color='#1f77b4'
        # ))
        
        # # Fit KDE
        # kde = KernelDensity(bandwidth=1.0, kernel='gaussian')
        # kde.fit(years.reshape(-1, 1))
        
        # # Generate points for KDE curve
        # x_grid = np.linspace(years.min(), years.max(), 100).reshape(-1, 1)
        # log_dens = kde.score_samples(x_grid)
        # dens = np.exp(log_dens)
        
        # # Add KDE curve
        # fig.add_trace(go.Scatter(
        #     x=x_grid.flatten(),
        #     y=dens,
        #     name='KDE',
        #     line=dict(color='#ff7f0e', width=2)
        # ))
        
        # # Update layout
        # # Adjust layout based on full screen status
        # margin_values = dict(l=40, r=40, t=40, b=40)
        # height = 600 if is_full_screen else None
        
        # fig.update_layout( 
        #     margin=margin_values,
        #     height=height,
        #     xaxis_title='Release Year',
        #     yaxis_title='Probability Density',
        #     showlegend=True,
        #     legend=dict(
        #         yanchor="top",
        #         y=0.99,
        #         xanchor="left",
        #         x=0.01
        #     )
        # )
        
        # # Add statistical information
        # stats_text = f"""
        # Statistics:
        # Mean Year: {np.mean(years):.1f}
        # Median Year: {np.median(years):.1f}
        # Mode Year: {float(np.bincount(years.astype(int)).argmax())}
        # Standard Deviation: {np.std(years):.1f}
        # """
        
        with ui.row().classes('w-full'):
            ui.plotly(fig).classes('w-full h-64')
            # if is_full_screen:
            #     ui.label(stats_text).classes('w-full text-sm')
            
    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')