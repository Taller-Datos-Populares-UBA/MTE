import dash
import dash_bootstrap_components as dbc

# meta_tags are required for the app layout to be mobile responsive
external_scripts = ["https://cdn.plot.ly/plotly-locale-es-latest.js"] # Agregamos español como lenguaje
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.LITERA],
                external_scripts=external_scripts,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

# Para que no tire error al principio por las callbacks cruzadas
# app.config.suppress_callback_exceptions = True
