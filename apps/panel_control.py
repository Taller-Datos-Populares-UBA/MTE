from datetime import date, datetime

# import pandas as pd

import plotly.graph_objects as go
# import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
# from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
from dash.dependencies import Output, Input, State
# from future.utils import ensure_new_type
# from dash.exceptions import PreventUpdate

# import sys
# sys.path.append("..")

from utils.utils_panel import *
# from utils.utils_panel import predios

from app import app

predios = df.predio.unique()


rutas = [
    'R8', 'R16', 'R12', 'E2C', 'E1', 'E2B', 'RIS', 'E5', 'E10', 'EVU',
    'E13', 'Avellaneda (A)', 'Avellaneda (C)', 'Avellaneda (D)',
    'Avellaneda (F)', 'Avellaneda (E)', 'Avellaneda (B)', 'R1', 'R5',
    'R11', 'E8C', 'R14', 'R26', 'R22', 'R25', 'R3', 'E8A ', 'E8B',
    'R6', 'R7', 'R9', 'R15', 'R17', 'R20', 'R21', 'R24', 'E2A',
]

materiales = df.material.unique()

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# print(df.predio.unique())


# app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)

# app.title = "Tablero MTE"
# Para que no tire error al principio por las callbacks cruzadas
# app.config.suppress_callback_exceptions = True

layout = html.Div([
    html.Div(id="altura-navbar", style={"height": "45px"}),
    html.Div(id="div-izquierda", children=[
        html.Img(
            src=app.get_asset_url("logo_negro.png"), className="logo-mte-panel"
        ),
        html.Label("Elegí el rango de fechas"),
        dcc.DatePickerRange(
            id="date-range",
            display_format="D/M/Y",
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2021, 12, 31),
            start_date=date(2019, 5, 15),
            end_date=date(2021, 8, 10),
        ),
        html.Label("Elegí el predio"),
        dcc.Dropdown(
            id="dropdown-predios",
            options=[
                {"label": predio.capitalize(), "value": predio} for predio in predios
            ],
            value=predios,
            multi=True  # Por ahora lo apago para que funcione la versión preliminar pero después lo necesitamos
        ),
        html.H6(id="salida-predios"),
        html.Label("Elegí la ruta o etapa"),
        dcc.Dropdown(
            id="dropdown-rutas",
            options=
            [{"label": "Todas", "value": "TODAS"}]+[{"label": ruta.capitalize(), "value": ruta} for ruta in rutas],
            
            multi=True,
            value=["TODAS"],
        ),
        html.H6(id="salida-rutas"),
        html.Label("Elegí el tipo de material"),
        dcc.Dropdown(
            id="dropdown-materiales",
            options=
            [{"label": material.capitalize(), "value": material} for material in materiales],
            
            multi=True,
            value=materiales,
        ),
        html.H6(id="salida-materiales"),
        html.Label("Elegí el tipo de cartonere"),
        dcc.Dropdown(
            id="dropdown-cartonere",
            options=[
                dict(label="LE", value="LE"),
                dict(label="RA", value="RA"),
                dict(label="No especificado", value="No especificado")
            ],
            multi=True,
            value=["LE", "RA", "No especificado"],
        ),
        html.Button(
            id="btn-filtro",
            children="Filtrar",
            n_clicks=0,
            className="btn-filtro"
        )


    ], style={"display": "inline-block", "width": "30%"}
    ),
    html.Div(id="div-derecha", children=[
    dcc.Tabs(id="tabs",
        children=[
            dcc.Tab(label="Pestaña 1", value="tab_1",
            children=[
                html.H1("esta es la tab 1"),
                html.Div("Peso total: 1500kg"),
                dcc.Graph(id="grafico-historico"),
                dcc.Graph(id="grafico-torta")
            ]),
            dcc.Tab(label="Pestaña 2", value="tab_2",
            children=[
                html.H1("esta es la tab 2"),
                dash_table.DataTable(
                    id="tabla",
                    editable=True,
                    columns=[{"name": i, "id": i} for i in df.columns],
                    # data=df.to_dict('records'),
                )
            ]),
        ],
        value="tab_1"
    ),
    html.Div(id="salida-tabs"),
    ], style={"width": "70%", "display": "inline-block", "float": "right"}
    ),

])


# @app.callback(
#     Output("salida-tabs", "children"),
#     Input("tabs", "value")
# )
# def render_content(value):
#     if value == "tab_1":
#         return html.Div([
#             html.H1("esta es la tab 1"),
#             dcc.Graph(id="grafico-historico"),
#             dcc.Graph(id="grafico-torta")
#         ])
#     else:
#         return html.H1("esta es la tab 2"),


@app.callback(
    [
        Output("grafico-historico", "figure"),
        Output("grafico-torta", "figure"),
        Output("tabla", "data")
    ],
    [
        Input("btn-filtro", "n_clicks"),
        State("dropdown-predios", "value"),
        State("dropdown-rutas", "value"),
        State("dropdown-materiales", "value"),
        State("dropdown-cartonere", "value"),
        State("date-range", "start_date"),
        State("date-range", "end_date"),
    ]
)
def filtrar(n_clicks, predios, rutas, materiales, cartonere, fecha_inicio, fecha_fin):
    """
    Se ejecuta al principio y cada vez que se clickee el botón.
    """
    global df
    # if n_clicks >= 0:
    df_filtrado = crear_df_filtrado(df, predios, datetime.fromisoformat(fecha_inicio), datetime.fromisoformat(fecha_fin), materiales, cartonere)
    fig_hist = pesos_historico(df_filtrado, operacion="suma")
    fig_torta = torta(df_filtrado)
    return fig_hist, fig_torta, df_filtrado.to_dict("records")
    # else:
    #     raise PreventUpdate
