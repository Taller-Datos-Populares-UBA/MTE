import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import State
from dash_table import DataTable

from apps.base import *
from elements import CreateButton, SelectDates, SelectFilterOptions, CreateModal, CreateFilters
from mte_dataframe import MTEDataFrame
from utils.utils import crear_df_filtrado, crear_tabla
from utils.utils_panel import pesos_historico_promedio, torta, pesos_historico_predios, datos_tabla

from dashpanelcontrolhandler import DashPanelControlHandler

# Cards

tabla_resumen = crear_tabla(
    id = "tabla-Resumen",
    titulos_columnas = {
        "clasificacion": "Clasificación",
        "peso": "Peso (kg)"
    },
    tipos = {"peso": "numeric"},
    dimensiones = ("auto", "200px")
    )

fig_vacio = go.Figure()
fig_vacio.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=10,
)
fig_vacio.update_xaxes(
    zeroline=False,
    showgrid=False,
    tickmode="array",
    tickvals=[],
    ticktext=[]
)
fig_vacio.update_yaxes(
    zeroline=False,
    showgrid=False,
    tickmode="array",
    tickvals=[],
    ticktext=[]
)

graph_hist = dcc.Graph(id="grafico-historico", figure=fig_vacio,
                       config={'displaylogo': False, 'displayModeBar': False, 'locale': 'es'})
graph_torta = dcc.Graph(id="grafico-torta", figure=fig_vacio,
                        config={'displaylogo': False, 'displayModeBar': False, 'locale': 'es'})
graph_barras = dcc.Graph(id="grafico-barras", figure=fig_vacio,
                         config={'displaylogo': False, 'displayModeBar': False, 'locale': 'es'})

card_resumen = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Resumen", id="monto-card-saldo", className="card-title"),
            html.Div(children=[
                tabla_resumen],
                id="tabla-resumen-parent")]

    )], className="card"
)

card_historico = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Gráfico temporal", className="card-title"),
            html.P("Promedio por 2 semanas", className="card-subtitle"),
            graph_hist,
        ],

    )], className="card last-card",
)

card_torta = dbc.Card([
    dbc.CardBody(
        [
            html.H5("Porcentajes", className="card-title"),
            graph_torta
        ],
    )], className="card"
)

card_barras = dbc.Card([
    dbc.CardBody(
        [
            html.H5("Distribución por fecha", className="card-title"),
            graph_barras
        ],
    )], className="card"
)

cards_panel = html.Div(
    [
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Row(children=[
                            dbc.Col(card_resumen, width=6
                                    ),
                            dbc.Col(card_torta, width=6
                                    )
                        ]),
                        dbc.Col(card_barras,
                                ),
                        dbc.Col(card_historico
                                ),
                    ],
                    width=12
                ),
            ],
            id="ro1"
        ),
    ]
)


def layout(predios, rutas, materiales, cartoneres):
    return html.Div([

        CreateModal("sininfopanel", "No se encontró información",
                    "Revisá si estan correctamente seleccionados los filtros."),
        html.Div(id="div-izquierda-panel", className="botonera", children=[
            CreateFilters(predios, rutas, materiales, cartoneres),
            CreateButton("btn-filtro", "Filtrar"),

        ],
                 ),
        html.Div(id="div-derecha", className="output", children=[
            html.Div(className="tabs-panel-parent", children=[
                html.Div([
                    html.Div(children=[
                        html.Div(id="warning-subir-archivo"),
                        html.Label('Agrupar por:', className="labels"),
                        dcc.Dropdown(
                            id='dropdown_clasificador_vistas',
                            className="dropdowns",
                            options=[
                                {"label": 'Predio', "value": 'predio'},
                                {"label": 'Material', "value": 'material'},
                            ],
                            value='predio',
                            multi=False
                        ), ]
                    ),
                    dcc.Loading(
                        id="loading-1",
                        children=[html.Div(className="graficos-div-parent", children=[
                            cards_panel
                        ])],
                        type="circle",
                    ),
                ], className="panel-container")
            ],
                     ),
        ])

    ])


dash_handler_panel = DashPanelControlHandler(tabla_resumen.columns)


@app.callback(
    [
        Output("grafico-historico", "figure"),
        Output("grafico-torta", "figure"),
        Output("grafico-barras", "figure"),
        Output("sininfopanel-modal", "is_open"),
        Output("tabla-Resumen", "data"),

    ],
    [
        Input("dropdown_clasificador_vistas", "value"),
        State("dropdown-predios", "value"),
        State("dropdown-rutas", "value"),
        State("dropdown-materiales", "value"),
        State("dropdown-cartonere", "value"),
        State("date-range", "start_date"),
        State("date-range", "end_date"),

    ],
    prevent_initial_call=True
)
def filtrar(clasificador, predios, rutas, materiales, cartonere, fecha_inicio,
            fecha_fin):
    trigger = callback_context.triggered[0]

    return dash_handler_panel.panel_control(trigger, clasificador, predios, rutas, materiales, cartonere, fecha_inicio,
                                            fecha_fin)
