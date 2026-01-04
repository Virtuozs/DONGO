from dash import Dash
import dash_bootstrap_components as dbc
from layouts.page1_overview import layout
from callbacks.page1_callbacks import register_callbacks

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)

app.layout = layout()
register_callbacks(app)

server = app.server

if __name__ == "__main__":
    app.run(debug=True)
