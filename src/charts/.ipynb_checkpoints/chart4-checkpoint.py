from nicegui import ui
import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet

def create_chart4(app_state, **kwargs):
    """Streams Trend Over Time with Prophet Forecast up to 2028"""
    ui.label('Streams Trend Over Time with Prophet Forecast').classes('text-h6 hidden')

    if app_state.filtered_data is None or app_state.filtered_data.empty:
        ui.label('No data available')
        return

    try:
        # Ensure columns are numeric
        app_state.filtered_data['streams'] = pd.to_numeric(app_state.filtered_data['streams'], errors='coerce')
        app_state.filtered_data['released_year'] = pd.to_numeric(app_state.filtered_data['released_year'], errors='coerce')
        app_state.filtered_data['released_month'] = pd.to_numeric(app_state.filtered_data['released_month'], errors='coerce')
        app_state.filtered_data['released_day'] = pd.to_numeric(app_state.filtered_data['released_day'], errors='coerce')

        # Fill missing date parts
        app_state.filtered_data.loc[:, 'released_year'].fillna(2000, inplace=True)
        app_state.filtered_data.loc[:, 'released_month'].fillna(1, inplace=True)
        app_state.filtered_data.loc[:, 'released_day'].fillna(1, inplace=True)

        # Clip month and day values within valid ranges
        app_state.filtered_data.loc[:, 'released_month'] = app_state.filtered_data['released_month'].clip(1, 12).astype(int)
        app_state.filtered_data.loc[:, 'released_day'] = app_state.filtered_data['released_day'].clip(1, 31).astype(int)

        # Rename columns and create a datetime column
        date_renamed = app_state.filtered_data.rename(
            columns={'released_year': 'year', 'released_month': 'month', 'released_day': 'day'}
        )
        date_renamed['date'] = pd.to_datetime(date_renamed[['year', 'month', 'day']], errors='coerce')

        # Drop invalid dates
        date_renamed = date_renamed.dropna(subset=['date'])

        # Aggregate streams by date
        trend_data = date_renamed.groupby('date')['streams'].sum().reset_index()

        # Prepare data for Prophet: rename columns to ds (date) and y (target)
        prophet_data = trend_data.rename(columns={'date': 'ds', 'streams': 'y'})

        # Initialize and fit the Prophet model
        model = Prophet(yearly_seasonality=True)
        model.fit(prophet_data)

        # Determine the last year in the historical data
        last_date = prophet_data['ds'].max()
        last_year = last_date.year

        # Generate future dates: January 1st of each year from last_year+1 to 2028
        forecast_years = [year for year in range(last_year + 1, 2029)]
        future_dates = pd.to_datetime([f"{year}-01-01" for year in forecast_years])
        future_df = pd.DataFrame({'ds': future_dates})

        # Merge historical dates with future dates
        full_future = pd.concat([prophet_data[['ds']], future_df], ignore_index=True)

        # Generate the forecast
        forecast = model.predict(full_future)[['ds', 'yhat']]

        # Create the figure
        fig = go.Figure()

        # Add actual streams
        fig.add_trace(go.Scatter(
            x=prophet_data['ds'],
            y=prophet_data['y'],
            mode='lines',
            name='Actual Streams',
            line=dict(color='blue', width=1)
        ))

        max_year = app_state.filtered_data['released_year'].max()
        x0_date = pd.to_datetime(f"{max_year}-01-01").isoformat()
        x1_date = pd.to_datetime(f"{max_year + 5}-01-01").isoformat()
        
        fig.add_vrect(
            x0=x0_date, x1=x1_date,
            fillcolor="rgba(255, 0, 0, 0.1)", opacity=0.5,
            layer="below", line_width=0,
            annotation_text="Prediction Area",
            annotation_position="top right",
        )
        
        # Add Prophet forecast
        fig.add_trace(go.Scatter(
            x=forecast['ds'],
            y=forecast['yhat'],
            mode='lines',
            name='Prophet Prediction',
            line=dict(color='red', width=1)
        ))

        # Update layout
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Streams',
            hovermode='x unified',
            legend=dict(x=0, y=1, traceorder='normal')
        )

        with ui.row().classes('w-full'):
            ui.plotly(fig).classes('w-full')

    except Exception as e:
        ui.label(f'Error creating chart: {str(e)}')
