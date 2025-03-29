from nicegui import ui
import pandas as pd
import plotly.express as px

def create_chart4(app_state, **kwargs):
    """Streams Trend Over Time with ML Trend Line"""
    ui.label('Streams Trend Over Time').classes('text-h6 hidden')

    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return

    try:
        # Ensure columns are numeric
        app_state.filtered_data['streams'] = pd.to_numeric(app_state.filtered_data['streams'], errors='coerce')
        app_state.filtered_data['released_year'] = pd.to_numeric(app_state.filtered_data['released_year'], errors='coerce')
        app_state.filtered_data['released_month'] = pd.to_numeric(app_state.filtered_data['released_month'], errors='coerce')
        app_state.filtered_data['released_day'] = pd.to_numeric(app_state.filtered_data['released_day'], errors='coerce')

        # Avoid chained assignment
        app_state.filtered_data.loc[:, 'released_year'].fillna(2000, inplace=True)
        app_state.filtered_data.loc[:, 'released_month'].fillna(1, inplace=True)
        app_state.filtered_data.loc[:, 'released_day'].fillna(1, inplace=True)

        # Clip date values within valid ranges
        app_state.filtered_data.loc[:, 'released_month'] = app_state.filtered_data['released_month'].clip(1, 12).astype(int)
        app_state.filtered_data.loc[:, 'released_day'] = app_state.filtered_data['released_day'].clip(1, 31).astype(int)

        # Match pandas date expectations
        date_renamed = app_state.filtered_data.rename(
            columns={'released_year': 'year', 'released_month': 'month', 'released_day': 'day'}
        )

        # Create a datetime column
        date_renamed['date'] = pd.to_datetime(
            date_renamed[['year', 'month', 'day']],
            errors='coerce'
        )

        # Drop invalid dates
        date_renamed = date_renamed.dropna(subset=['date'])

        # Aggregate streams by date
        trend_data = date_renamed.groupby('date')['streams'].sum().reset_index()

        # Apply ML-based smoothing (30-day moving average)
        trend_data['smoothed_trend'] = trend_data['streams'].rolling(window=30, min_periods=1).mean()

        # Create the line chart
        fig = px.line(
            trend_data,
            x='date',
            y=['streams', 'smoothed_trend'],
            labels={'value': 'Streams', 'date': 'Release Date'},
            line_shape='linear',
            markers=True
        )

        # Improve visual readability
        fig.update_traces(
            selector=dict(name='streams'), line=dict(color='blue', width=2), name='Actual Streams'
        )
        fig.update_traces(
            selector=dict(name='smoothed_trend'), line=dict(color='green', width=3, dash='dash'), name='Trend Line'
        )

        # Update layout
        fig.update_layout(
            xaxis_title='Release Date',
            yaxis_title='Total Streams',
            xaxis=dict(showgrid=True),
            yaxis=dict(showgrid=True),
            hovermode='x unified'
        )

        with ui.row().classes('w-full'):
            ui.plotly(fig).classes('w-full')

    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
