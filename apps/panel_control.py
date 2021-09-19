from datetime import date, datetime, timedelta

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash import callback_context
from dash.dependencies import Output, Input, State

import utils.utils_panel as utils_panel
from app import app
from mte_dataframe import MTEDataFrame

from elements import CreateButton, SelectDates, SelectFilterOptions


df = MTEDataFrame.get_instance()
predios, rutas, materiales, cartoneres=MTEDataFrame.create_features()

# Cards
pago=1234
first_card = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Resumen", id="monto-card-saldo",className="card-title"),
            #html.P(f"$ {round(pago, 2)}", id="label-legajo"),
        ]
    )],className="card"
)


third_card = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Gráfico temporal",className="card-title"),
            dcc.Graph(id="grafico-historico"),
        ],
    
    )],className="card",
)

second_card = dbc.Card([
    dbc.CardBody(
        [
            html.H5("Distribución", className="card-title"),
            dcc.Graph(id="grafico-torta")
        ],
    )], className="card"
)

cards_panel = html.Div(
    [
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Col(
                            first_card,
                        ),
                        dbc.Col(
                            second_card,
                        ),
                        dbc.Col(
                            third_card
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

    html.Div(id="div-izquierda-panel", className="botonera",children=[
        html.Img(
            src=app.get_asset_url("logo_negro.png"), className="logo-mte-panel"
        ),
        SelectDates("date-range-panel","radio-button-fechas-panel"),
        SelectFilterOptions(predios, "Elegí el predio", "dropdown-predios", "salida-predios", capitalize=True),
        SelectFilterOptions(rutas, "Elegí la ruta o etapa", "dropdown-rutas", "salida-rutas", add_all_as_option=True),
        SelectFilterOptions(materiales, "Elegí el tipo de material", "dropdown-materiales", "salida-materiales",
                            capitalize=True),
        SelectFilterOptions(cartoneres, "Elegí el tipo de cartonere", "dropdown-cartonere", "salida-cartoneres"),

        CreateButton("btn-filtro","Filtrar"),

    ],
             ),
    html.Div(id="div-derecha",className="output",children=[
        html.Div(className="tabs-panel-parent",children=[
        dcc.Tabs(id="tabs",
                 children=[
                     dcc.Tab(label="Pestaña 1", value="tab_1",
                             children=[
                                 html.Div(children=[
			          html.Label('Ver por:',className="labels"),
        			  dcc.Dropdown(
            				id='dropdown_clasificador_vistas',
            				className="dropdowns",
            				options=[
                			{"label": 'Material', "value": 'material'},
                			{"label": 'Etapa', "value": 'etapa'}, 
            				],
            				value='material',
            				multi=False
        ),]
    	),
        html.Div(className="graficos-div-parent",children=[
    		 		  cards_panel,
    	                         html.Div("Peso total: 1500kg"),
                             ]),
        ]),
                    # dcc.Tab(label="Pestaña 2", value="tab_2",
                    #         children=[
                    #             dash_table.DataTable(
                    #                 id="tabla",
                    #                 editable=True,
                    #                 columns=[{"name": i, "id": i} for i in df.columns],
                    #             )
                    #         ]),
                 ],
                 value="tab_1"
                 ),
    ],
             ),
    ])

])

@app.callback(
    [
        Output("date-range-panel","start_date"),
        Output("date-range-panel","end_date"),
        Output("radio-button-fechas-panel","value")
    ],
    [
        Input("radio-button-fechas-panel","value"),
        Input("date-range-panel","start_date"),
        Input("date-range-panel","end_date"),
    ]
)
def cambiarFechaCalendario(periodo,start_date,end_date):
    trigger = callback_context.triggered[0]

    if trigger["prop_id"] == "date-range-panel.start_date" or trigger["prop_id"] == "date-range-panel.end_date" :
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

    return fecha_inicio,fecha_finalizacion,periodo


@app.callback(
    [
        Output("grafico-historico", "figure"),
        Output("grafico-torta", "figure"),
        #Output("tabla", "data")
    ],
    [
        Input("btn-filtro", "n_clicks"),
        State("dropdown-predios", "value"),
        State("dropdown-rutas", "value"),
        State("dropdown-materiales", "value"),
        State("dropdown-cartonere", "value"),
        State("date-range-panel", "start_date"),
        State("date-range-panel", "end_date"),
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
    return fig_hist, fig_torta #df_filtrado.to_dict("records")
