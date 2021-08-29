#Importaciones
# from datetime import date, datetime
import pandas as pd
# import plotly.express as px
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
# from dash_table import DataTable, FormatTemplate
from dash.dependencies import Output, Input, State
from dash import callback_context
# import base64
# import time
# import plotly.graph_objects as go
from utils.utils_finanzas import *
# from future.utils import ensure_new_type

from apps import panel_control, finanzas

from app import app
# from app import server

#prevent_initial_callbacks para evitar que se llamen las funciones al principio y Update_title para cuando se ejecutan los callbacks
# app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LITERA],external_scripts=["https://cdn.plot.ly/plotly-locale-es-latest.js"],prevent_initial_callbacks=True,update_title="Cargando")
# app.title = "Financias MTE"
# app.config.suppress_callback_exceptions = True

"""
----------------------------------------------------------------------------------------------------------------------------------------------

Estructuras recurrentes

----------------------------------------------------------------------------------------------------------------------------------------------

"""

#Estructura del navbar: ul -> li -> a -> img + p
navbar = (
	html.Ul([
		html.Li([
			html.A([
				html.Img(
					src=app.get_asset_url("settings.svg")
				),
                # dcc.Link("Panel de Control", href="/apps/panel_control")
				html.P("Panel de Control")
			],
            href="/panel_control"
            )
		]),

		html.Li([
			html.A([
				html.Img(
					src=app.get_asset_url("money.svg")
				),

				html.P("Finanzas")
			],
            href="/finanzas",
            # className="link-active",
            )
		]),

		html.Li([
			html.A([
				html.Img(
					src=app.get_asset_url("tune.svg")
				),
				html.P("Base de datos")
			])
		]),

		html.Li([
			html.A(
				html.Img(
					src=app.get_asset_url("logo_blanco.png"), 
					className="logo-mte-finanzas",
					id="logo-mte-finanzas",
					),
				href="https://mteargentina.org.ar/"
			)
		]), 

	], id="navbar")
)


app.layout = html.Div([
    # Para manejar las distintas páginas/rutas
    dcc.Location(id='url', refresh=True),
    navbar,
    # dcc.Link("probando finanzas", href="/finanzas"),
    html.Div(id="page-content", children=[])
    ]
)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/panel_control':
        return panel_control.layout
    elif pathname == '/finanzas':
        return finanzas.layout
    # else:
    #     return finanzas.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == "__main__":
    app.run_server(debug=True, port=9050)

#1) Logica de tomar fecha de la computadora para devolver la ultima semana, mes, año.
#2) Logica para conseguir tambien la fecha y automaticamente colocarla para una semana antes en el calendario de "Otro"
#3) Logica del return del callback de ambas Tabs.