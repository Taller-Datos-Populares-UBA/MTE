import dash
import dash_bootstrap_components as dbc

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True, prevent_initial_callbacks=True,
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.LITERA],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
# server = app.server
