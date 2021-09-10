from datetime import date, datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, Input, State

import utils.utils_panel as utils_panel
from app import app
from mte_dataframe import MTEDataFrame

df = MTEDataFrame.get_instance()
predios, rutas, materiales, cartoneres=MTEDataFrame.create_features()

# Cards
pago=1234
first_card = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Resumen", id="monto-card-saldo"),
            dcc.Tab(label="Pestaña 2", value="tab_2",
                             children=[
                                 dash_table.DataTable(
                                     id="tabla",
                                     editable=True,
                                     columns=[{"name": i, "id": i} for i in df.columns],
                                 )
                             ]),
            #html.P(f"$ {round(pago, 2)}", id="label-legajo"),
        ]
    )]
)


third_card = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Gráfico temporal"),
            dcc.Graph(id="grafico-historico"),
        ],
    className="card",
    )]
)

second_card = dbc.Card([
    dbc.CardBody(
        [
            html.H5("Distribución", className="card-title"),
            dcc.Graph(id="grafico-torta")
        ],
    className="card"
    )]
)

cards_panel = html.Div(
    [
        dbc.Col(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(first_card,),
                        dbc.Col(second_card,)
                    ],

                ),
                dbc.Col(third_card),
            ],
            id="ro1"
        ),
    ]
)


def CreateButton(identificacion,txt):
    return html.Div([
        html.Button(
            children=[
                html.Img(
                    src=app.get_asset_url("search.svg")
                ),

                html.P(
                    txt
                )
                ],
            id=identificacion,
            n_clicks=0,
            className="mr-1 mt-1 btn btn-primary search-button"

        ),
    ],
    className="button-container")

def SelectDates(identificacion):
    return html.Div(children=[
            html.Label("Elegí el rango de fechas",className="labels"),
            html.Div([
                dbc.RadioItems(
                        options=[
                                {'label': 'Última semana', 'value': 'semana'},
                                {'label': 'Último mes', 'value': 'mes'},
                                {'label': 'Último año', 'value': 'año'},
                                {'label': 'Otro', 'value': 'otro'}
                        ],
                        value='semana',
                        className="radio-item",
                        style={
                                "fontSize": "18px",
                                "width": "100%",
                        },
                        id="radio-button-fechas"
                ),    
                dcc.DatePickerRange(
                    id=identificacion,
                    display_format="D/M/Y",
                    min_date_allowed=date(1995, 8, 5),
                    max_date_allowed=date(2021, 12, 31),
                    start_date=date(2019, 5, 15),
                    end_date=date(2021, 8, 10),
                )
                ],className="dates-container"
                )
    ])


def SelectFilterOptions(options, label, dropdown_id, response_id, add_all_as_option=False, capitalize=False):
    options = list(options) + ["Todas"] if add_all_as_option else options
    initial_value = "Todas" if add_all_as_option else options
    return html.Div(children=[
        html.Label(label,className="labels"),
        dcc.Dropdown(
            id=dropdown_id,
            className="dropdowns",
            options=[
                {"label": option.capitalize() if capitalize else option, "value": option} for option in options
            ],
            value=initial_value,
            multi=True
        ),
        html.H6(id=response_id)]
    )


layout = html.Div([
    html.Div(id="altura-navbar", style={"height": "45px"}),
    html.Div(id="div-izquierda", children=[
        html.Img(
            src=app.get_asset_url("logo_negro.png"), className="logo-mte-panel"
        ),
        SelectDates("date-range"),
        SelectFilterOptions(predios, "Elegí el predio", "dropdown-predios", "salida-predios", capitalize=True),
        SelectFilterOptions(rutas, "Elegí la ruta o etapa", "dropdown-rutas", "salida-rutas", add_all_as_option=True),
        SelectFilterOptions(materiales, "Elegí el tipo de material", "dropdown-materiales", "salida-materiales",
                            capitalize=True),
        SelectFilterOptions(cartoneres, "Elegí el tipo de cartonere", "dropdown-cartonere", "salida-cartoneres"),

        CreateButton("btn-filtro","Filtrar"),

    ], style={"display": "inline-block", "width": "30%"}
             ),
    html.Div(id="div-derecha", children=[
        dcc.Tabs(id="tabs",
                 children=[
                     dcc.Tab(label="Pestaña 1", value="tab_1",
                             children=[
                                 html.Div(children=[
			          html.Label('Ver por...',className="labels"),
        			  dcc.Dropdown(
            				id='dropdown_clasificador_vistas',
            				className="dropdowns",
            				options=[
                			{"label": 'Material', "value": 'material'},
                			{"label": 'Etapa', "value": 'etapa'}, 
            				],
            				value='material',
            				multi=False
        ),
        html.H6(id='dropdown_clasificador_vistas_content')]
    	),
    		 		  cards_panel,
    	                         html.Div("Peso total: 1500kg"),
                                 #dcc.Graph(id="grafico-historico"),
                                 #dcc.Graph(id="grafico-torta")
                             ]),
                     dcc.Tab(label="Pestaña 2", value="tab_2",
                             children=[
                                 dash_table.DataTable(
                                     id="tabla",
                                     editable=True,
                                     columns=[{"name": i, "id": i} for i in df.columns],
                                 )
                             ]),
                 ],
                 value="tab_1"
                 ),
        html.Div(id="salida-tabs"),
    ], style={"width": "70%", "display": "inline-block", "float": "right"}
             ),

])


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

    df = MTEDataFrame.get_instance()
    df_filtrado = utils_panel.crear_df_filtrado(df, predios, datetime.fromisoformat(fecha_inicio),
                                                datetime.fromisoformat(fecha_fin), materiales, cartonere)
    fig_hist = utils_panel.pesos_historico(df_filtrado, operacion="suma")
    fig_torta = utils_panel.torta(df_filtrado)
    return fig_hist, fig_torta, df_filtrado.to_dict("records")
