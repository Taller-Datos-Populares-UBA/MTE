from datetime import date, datetime, timedelta

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash import callback_context
from dash.dependencies import Output, Input, State
from dash_table import DataTable


from utils.utils import crear_df_filtrado
from utils.utils_panel import pesos_historico_promedio, torta, pesos_historico_predios, pesos_historico_materiales, datos_tabla

from app import app
from mte_dataframe import MTEDataFrame

from elements import CreateButton, SelectDates, SelectFilterOptions, CreateModal

if MTEDataFrame.FILES_TO_LOAD:
    predios, rutas, materiales, cartoneres = MTEDataFrame.create_features()
else:
    predios = ['CORTEJARENA', 'SAAVEDRA', 'No especificado', 'BARRACAS', 'AVELLANEDA']
    rutas = [
        'R26', 'E5', 'EVU', 'E13', 'E2', 'E1', 'RAZ', 'E8', 'E10', 'R11', 'R14',
        'R4', 'R24', 'R5', 'R1', 'R12', 'R16', 'R6', 'R17', 'R21', 'R22', 'R3',
        'R9', 'R25', 'R20', 'R7', 'R8', 'R15', 'R18', 'RUTAS', 'AVELLANEDA',
        'CHACARITA', 'E2C', 'E2B', 'RIS', 'Avellaneda (A)', 'Avellaneda (C)',
        'Avellaneda (D)', 'Avellaneda (F)', 'Avellaneda (E)', 'Avellaneda (B)',
        'E8C', 'E8A ', 'E8B', 'E2A'
    ]
    materiales = ['No especificado', 'Mezcla B', 'Vidrio B', 'TELA', 'Chatarra', 'Papel Blanco B']
    cartoneres = ['LE', 'RA', 'No especificado']


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
        # html.Img(
        #    src=app.get_asset_url("logo_negro.png"), className="logo-mte-panel"
        #),

        html.H6(  # Titulo Botonera
                "Filtros",
                className="title-botonera"
        ),

        SelectDates("date-range-panel", "radio-button-fechas-panel"),
        SelectFilterOptions(predios, "Elegí el predio", "dropdown-predios", "salida-predios", capitalize=True),
        SelectFilterOptions(rutas, "Elegí la ruta o etapa", "dropdown-rutas", "salida-rutas", add_all_as_option=True),
        SelectFilterOptions(materiales, "Elegí el tipo de material", "dropdown-materiales", "salida-materiales",
                            capitalize=True),
        SelectFilterOptions(cartoneres, "Elegí el tipo de cartonere", "dropdown-cartonere", "salida-cartoneres"),

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
        Output("date-range-panel", "start_date"),
        Output("date-range-panel", "end_date"),
        Output("radio-button-fechas-panel", "value")
    ],
    [
        Input("radio-button-fechas-panel", "value"),
        Input("date-range-panel", "start_date"),
        Input("date-range-panel", "end_date"),
    ]
)
def cambiarFechaCalendario(periodo, start_date, end_date):
    trigger = callback_context.triggered[0]

    if trigger["prop_id"] == "date-range-panel.start_date" or trigger["prop_id"] == "date-range-panel.end_date":
        fecha_inicio = start_date
        fecha_finalizacion = end_date
        periodo = "otro"
    else:
        if periodo == 'otro':
            fecha_inicio = start_date
            fecha_finalizacion = end_date
        elif periodo == 'semana':
            fecha_finalizacion = date.today()
            otra_fecha = timedelta(6)
            fecha_inicio = fecha_finalizacion - otra_fecha
        elif periodo == 'mes':
            fecha_finalizacion = date.today()
            otra_fecha = timedelta(30)
            fecha_inicio = fecha_finalizacion - otra_fecha
        else:
            fecha_finalizacion = date.today()
            otra_fecha = timedelta(364)
            fecha_inicio = fecha_finalizacion - otra_fecha

    return fecha_inicio, fecha_finalizacion, periodo


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
        State("date-range-panel", "start_date"),
        State("date-range-panel", "end_date"),
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

    return fig_hist, fig_torta, fig_barras, open_sininfopanel_modal, tabla_resumen  # df_filtrado.to_dict("records")


@app.callback(
    Output("warning-subir-archivo", "children"),
    Input("btn-filtro", "n_clicks")
)
def warning_subir_archivo(n_clicks):
    """
    Agrega un warning si el usuario no cargó un archivo.
    """
    if n_clicks:
        if MTEDataFrame.FILES_TO_LOAD:
            return None
    if MTEDataFrame.FILES_TO_LOAD is None:
        return dbc.Alert("Por favor subir un archivo primero y luego apretar FILTRAR", color="danger", style={"font-size": "20px"})
