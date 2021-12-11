from datetime import datetime

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State
from dash_table import DataTable

from apps.base import *
from elements import CreateButton, SelectDates, SelectFilterOptions, CreateModal, CreateFilters
from mte_dataframe import MTEDataFrame
from utils.utils import crear_df_filtrado
from utils.utils_panel import pesos_historico_promedio, torta, pesos_historico_predios, datos_tabla

# Cards

card_resumen = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Resumen", id="monto-card-saldo", className="card-title"),
            html.Div(children=[
                DataTable(
                    id="tabla-Resumen",
                    columns=[{"name": "Clasificación", "id": "clasificacion"},
                             {"name": "Peso (kilos)", "id": "peso"}

                             ],
                    editable=False,
                    row_deletable=False,
                    style_cell={
                        "textOverflow": "ellipsis",
                        "whiteSpace": "nowrap",
                        "border": "1px solid black",
                        "border-left": "2px solid black"
                    },
                    style_header={
                        "backgroundColor": "#4582ec",
                        "color": "white",
                        "border": "0px solid #2c559c",
                    },
                    style_table={
                        "height": "200px",
                        "minHeight": "200px",
                        "maxHeight": "200px",
                        "overflowX": "auto"
                    },
                    fixed_rows={'headers': True},

                )],
                id="tabla-Resumen-parent")]

    )], className="card"
)


card_historico = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Gráfico temporal", className="card-title"),
            html.P("Promedio por 2 semanas", className="card-subtitle"),
            dcc.Graph(id="grafico-historico", config={'displaylogo': False, 'displayModeBar': True, 'locale': 'es'}),
        ],

    )], className="card",
)


card_torta = dbc.Card([
    dbc.CardBody(
        [
            html.H5("Porcentajes", className="card-title"),
            dcc.Graph(id="grafico-torta", config={'displaylogo': False, 'displayModeBar': False, 'locale': 'es'})
        ],
    )], className="card"
)

card_barras = dbc.Card([
    dbc.CardBody(
        [
            html.H5("Distribución por fecha", className="card-title"),
            dcc.Graph(id="grafico-barras", config={'displaylogo': False, 'displayModeBar': False, 'locale': 'es'})
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


layout = html.Div([

    CreateModal("sininfopanel", "No se encontró información", "Revisá si estan correctamente seleccionados los filtros."),
    html.Div(id="div-izquierda-panel", className="botonera", children=[
        CreateFilters(predios, rutas, materiales, cartoneres),
        CreateButton("btn-filtro", "Filtrar"),

    ],
        ),
    html.Div(id="div-derecha", className="output", children=[
        html.Div(className="tabs-panel-parent", children=[
            dcc.Tabs(id="tabs",
                     children=[
                         dcc.Tab(label="Panel de control", value="tab_1",
                                 children=[
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
                                 ]),
                         ],
                     value="tab_1"
                     ),
            ],
            ),
    ])

])

@app.callback(
    [
        Output("grafico-historico", "figure"),
        Output("grafico-torta", "figure"),
        Output("grafico-barras", "figure"),
        Output("sininfopanel-modal", "is_open"),
        Output("tabla-Resumen", "data"),

    ],
    [
        Input("btn-filtro", "n_clicks"),
        Input("close-modal-sininfopanel-button", "n_clicks"),
        Input("dropdown_clasificador_vistas", "value"),
        State("dropdown-predios", "value"),
        State("dropdown-rutas", "value"),
        State("dropdown-materiales", "value"),
        State("dropdown-cartonere", "value"),
        State("date-range", "start_date"),
        State("date-range", "end_date"),
        State("sininfopanel-modal", "is_open"),
        State("grafico-historico", "figure"),
        State("grafico-torta", "figure"),
        State("grafico-barras", "figure"),

    ],
    prevent_initial_call=True
)
def filtrar(n_clicks, close_sininfo_modal_button, clasificador, predios, rutas, materiales, cartonere, fecha_inicio,
            fecha_fin, open_sininfopanel_modal, fig_hist, fig_torta, fig_barras):
    """
    Se ejecuta al principio y cada vez que se clickee el botón.
    """
    if "Todas" in rutas: 
        rutas = None
        
    trigger = callback_context.triggered[0]

    if trigger["prop_id"] in ['.', "btn-filtro.n_clicks"] or trigger["prop_id"].split('.')[0]=="dropdown_clasificador_vistas":
        df = MTEDataFrame.get_instance()
        df_filtrado = crear_df_filtrado(df, predios, rutas, datetime.fromisoformat(fecha_inicio),
                                        datetime.fromisoformat(fecha_fin), materiales, cartonere)
        if df_filtrado.empty:
            open_sininfopanel_modal = not open_sininfopanel_modal
        else:
            fig_hist = pesos_historico_promedio(df_filtrado, clasificador)
            fig_torta = torta(df_filtrado, clasificador)
            fig_barras = pesos_historico_predios(df_filtrado, clasificador)
            tabla_resumen = datos_tabla(df_filtrado, clasificador)
            tabla_resumen = tabla_resumen.to_dict('records')

    elif trigger["prop_id"] in ['.', "btn-filtro.n_clicks"]:
        open_sininfopanel_modal = not open_sininfopanel_modal

    return fig_hist, fig_torta, fig_barras, open_sininfopanel_modal, tabla_resumen
