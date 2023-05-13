import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State

from apps.base import *
from dash_panel_control_handler import DashPanelControlHandler
from elements import CreateButton, CreateModal, CreateFilters, EmptyFigure
from utils.utils import crear_tabla

# Cards
tabla_resumen = crear_tabla(
    id="tabla-Resumen", 
    titulos_columnas={
        "clasificacion": "Clasificación",
        "peso": "Peso (kg)"
    },
    tipos={"peso": "numeric"}, 
    dimensiones=("auto", "200px"))
    
tabla_posta = crear_tabla(id="tabla-Posta", titulos_columnas={}, tipos={"peso": "numeric"}, dimensiones=("auto", "200px"))


dic_labels_columnas = {'predio':'Predio', 'material':'Material', 'tipoCartonero':'Tipo de Cartonere'}

fig = EmptyFigure()

graph_hist = dcc.Graph(id="grafico-historico", figure=fig,
                       config={'displaylogo': False, 'displayModeBar': False, 'locale': 'es'})
graph_torta = dcc.Graph(id="grafico-torta", figure=fig,
                        config={'displaylogo': False, 'displayModeBar': False, 'locale': 'es'})
graph_barras = dcc.Graph(id="grafico-barras", figure=fig,
                         config={'displaylogo': False, 'displayModeBar': False, 'locale': 'es'})

card_resumen = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Resumen", id="monto-card-saldo", className="card-title"),
            dcc.Dropdown(id="dropdown-resumen", className="dropdowns",
                            options = [
                                {"label": 'Predio', "value": 'predio'},
                                {"label": 'Material', "value": 'material'},
                                {"label": 'Tipo de Cartonere', "value": 'tipoCartonero'}
                            ], multi=True, placeholder="Seleccionar", value=["predio","material","tipoCartonero"]),
            html.Div(children=[
                tabla_posta],
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

        CreateModal("error3"),
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
        Output("error3-modal", "is_open"),
        Output("header-error3", "children"),
        Output("body-error3", "children"),
        Output("tabla-Resumen", "data"),
        Output("tabla-Posta", "titulos_columnas"),
    ],
    [
        Input("btn-filtro", "n_clicks"),
        Input("close-modal-error3-button", "n_clicks"),
        Input("dropdown_clasificador_vistas", "value"),
        Input("dropdown-resumen", "value"),
        State("dropdown-predios", "value"),
        State("dropdown-rutas", "value"),
        State("dropdown-materiales", "value"),
        State("dropdown-cartonere", "value"),
        State("date-range", "start_date"),
        State("date-range", "end_date"),

    ],
    prevent_initial_call=True
)
def filtrar(filtrar_button, close_modal, clasificador, columnas_resumen, predios, rutas, materiales, cartonere, fecha_inicio,
            fecha_fin):
    trigger = callback_context.triggered[0]
    titulos_columnas = {k:dic_labels_columnas[k] for k in columnas_resumen}
    titulos_columnas["peso"] = "Peso (kg)"
    return dash_handler_panel.callback(trigger, clasificador, columnas_resumen, predios, rutas, materiales, cartonere, fecha_inicio, fecha_fin), titulos_columnas
