from nicegui import ui, app


@ui.page("/")
def index():
    return ui.html("<h1>Hello World</h1>")

ui.run(port=8080, title="Spotify Visualization")