from nicegui import ui
import pandas as pd
from plotly.express import line
from include_data_preparation import app_state

def paint_distribution_of_released_year():
    with ui.card().classes('w-full'):
        ui.label("Distribution of Released Year")
        if app_state.is_data_loaded:
            df = pd.DataFrame(app_state.data)
            fig = line(df, x="released_year", y="in_spotify_playlists", title="Distribution of Released Year")
            ui.plotly(fig)
        else:
            ui.label("No data loaded")