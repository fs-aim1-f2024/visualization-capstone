from nicegui import ui, app
from include_data_preparation import paint_data_preparation, app_state
from include_01_distribution_of_released_year import paint_distribution_of_released_year

@ui.page("/")
def index():
    paint_data_preparation()
    paint_chart()

@ui.refreshable
def paint_chart(): 
    paint_distribution_of_released_year() 

if __name__ in ["__main__", "__mp_main__"]:
    ui.run(port=8080, title="Spotify Visualization")