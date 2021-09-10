from datetime import date, datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash import callback_context
from dash.dependencies import Output, Input, State
from dash_table import DataTable, FormatTemplate

import utils.utils_finanzas as utils_finanzas
from app import app
from mte_dataframe import MTEDataFrame

from apps.panel_control import SelectDates, SelectFilterOptions,CreateButton


# Carga de DataFrames
df = MTEDataFrame.get_instance()
predios, rutas, materiales, cartoneres=MTEDataFrame.create_features()


fig = utils_finanzas.grafico_torta(7023, df)
df_filtrado = df.dropna()[["fecha", "material", "peso"]].head(10)

# funcion para crear columna de tipo de cartonere

# funcion para calcular pago, dado el dataframe, un legacyId y el dataframe de precios


precio_material_dict = {'Mezcla B': [15], 'TELA': [20], 'Vidrio B': [25], 'Chatarra': [10], 'No especificado': [0]}
precio_material_df = pd.DataFrame.from_dict(precio_material_dict, orient='index')
df_precio = precio_material_df.reset_index()
df_precio.rename(columns={"index": "material", 0: "preciocompra"}, inplace=True)

predios_2 = ['CORTEJARENA', 'SAAVEDRA']
fecha_inicio = pd.to_datetime('3/11/2020', format='%d/%m/%Y')
fecha_finalizacion = pd.to_datetime('3/8/2021', format='%d/%m/%Y')

df_filtrado_2 = utils_finanzas.crear_df_filtrado(df, predios_2, fecha_inicio, fecha_finalizacion, [], [])

pago = utils_finanzas.calcular_pago(df_filtrado_2, '1967', df_precio)

# Cards
first_card = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Monto a pagar", id="monto-card-saldo"),
            html.P(f"$ {round(pago, 2)}", id="label-legajo"),
        ]
    )]
)

second_card = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Ultimas cargas"),
            html.Div(children=[
                DataTable(
                    id="tabla-legajo",
                    columns=[
                        {
                            'name': 'Fecha',
                            'id': 'fecha',
                            'deletable': False,
                            'renamable': False,
                        },
                        {
                            'name': 'Material',
                            'id': 'material',
                            'deletable': False,
                            'renamable': False,
                            "type": 'numeric',
                            "format": FormatTemplate.money(2)
                        },
                        {
                            'name': 'Peso',
                            'id': 'peso',
                            'deletable': False,
                            'renamable': False,
                            "type": 'numeric',
                            # "format":FormatTemplate.money(2)
                        }
                    ],
                    data=[df_filtrado.iloc[i].to_dict() for i in range(len(df_filtrado.index))
                          # {"material": df.material.head(10)
                          # ,"precioventa": "",
                          # "preciocompra": ""}
                          ],
                )
            ])
        ])],
    className="card",
)

third_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Material recolectado", className="card-title"),
            dcc.Graph(id="graph-legajo", figure=fig),
        ]),
    className="card"
)

cards_individual = html.Div(
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
                        )
                    ],
                    width=7
                ),
                dbc.Col(third_card, width=5),
            ],
            id="ro1"
        ),
    ]
)

# Tooltip de la tabla
tooltiptable = dbc.Tooltip(
    children=["En la tabla de más abajo se pueden cargar los valores. Los centavos van separados con ' . ' y ",
              "más abajo hay botones para guardar la información de la tabla y cargarla más adelante, además de agregar otras filas para más materiales", ],
    target="help-table",
    placement="left",
    id="tooltip-table",
    hide_arrow=True,
    autohide=False,
    delay={"hide": 1000},
    style={
        "fontSize": "15px",
        "fontFamily": "Rubik, sans",
    },
)

"""
----------------------------------------------------------------------------------------------------------------------------------------------

Layout de la app

----------------------------------------------------------------------------------------------------------------------------------------------

"""

layout = html.Div([

    # navbar,

    dbc.Modal(  # Modal sin informacion
        children=[
            dbc.ModalHeader(
                "No se encontró información",
                style={
                    "font-size": "30px"
                }
            ),

            dbc.ModalBody(
                "Revisá si está correctamente seleccionado el rango de fechas y el predio.",
                style={
                    "font-size": "20px"
                }
            ),

            dbc.ModalFooter(
                dbc.Button(
                    children=[
                        html.Img(
                            src=app.get_asset_url("close.svg"),
                            className="ico"),
                        "Cerrar"
                    ],
                    id="close-modal-sin-info-button",
                    className="mr-1 mt-1 btn btn-primary",
                    n_clicks=0,
                )
            ),
        ],
        id="sininfo-modal",
        is_open=False,
        backdrop="static"  # Modal sin informacion
    ),

    dbc.Modal(  # Modal error archivo #Modal archivo fallado
        children=[
            dbc.ModalHeader(
                "Problemas con el archivo",
                style={
                    "font-size": "30px"}
            ),

            dbc.ModalBody(
                "El archivo parece estar dañado, vacio, o con un formato no soportado. Ingresá los valores a mano.",
                style={
                    "font-size": "20px"
                }
            ),

            dbc.ModalFooter(
                dbc.Button(
                    children=[
                        html.Img(
                            src=app.get_asset_url("close.svg"),
                            className="ico"),
                        "Cerrar"],
                    id="close-modal-data-table-button",
                    className="mr-1 mt-1 btn btn-primary",
                    n_clicks=0,
                )
            ),
        ],
        id="tabla-error-modal",
        is_open=False,
        backdrop="static"
    ),

    dcc.Download(id="download"),

    # Filtros ------------------------------------------------------------------------------------------------------------------------

    html.Div(
        id="botonera",
        children=[

            html.H6(  # Titulo Botonera
                "Filtros",
                id="title-botonera"
            ),

            html.Div(
                children=[  # Radiobuttons y picker de fechas
            SelectDates("date-range-finanzas"),
            SelectFilterOptions(predios, "Elegí el predio", "dropdown-predios", "salida-predios", capitalize=True),
            ]
            ),
            SelectFilterOptions(rutas, "Elegí la ruta", "dropdown-rutas", "salida-rutas",add_all_as_option=True, capitalize=True),
#
#            html.Div(  # Dropdown de los predios
#                children=[
#                    dcc.Dropdown(
#                        id="dropdown-predios",
#                        options=[
#                            {"label": predio.capitalize(), "value": predio} for predio in predios
#                        ],
#                        multi=False,
#                        placeholder="Seleccionar un predio",
#                        className="dropdowns"
#                    )],
#                id="dropdown-predios-div",
#                className="div-dropdown"
#
#            ),

            SelectFilterOptions(cartoneres, "Elegí el tipo de cartonere", "dropdown-cartonerx", "salida-cartoneres"),

#            html.Div(  # Dropdown de lxs cartonerxs
#                children=[
#                    dcc.Dropdown(
#                        id="dropdown-cartonerx",
#                        options=[
#                            {"label": cartoneres, "value": cartoneres} for cartoneres in cartoneres
#                        ],
#                        multi=False,
#                        placeholder="Seleccionar un tipo de cartonerx",
#                        className="dropdowns"
#                    )],
#                id="dropdown-cartonerxs-div",
#                className="div-dropdown"
#
#            ),

            html.Label(  # Label de la tabla
                "Tabla de precios",
                id="label-tabla"
            ),

            html.P(  # Ayuda de la tabla
                html.Img(
                    src=app.get_asset_url("help.svg"),
                    id="help-ico"),
                id="help-table"
            ),

            tooltiptable,  # Ayuda emergente de la tabla

            html.Div(
                children=[  # Tabla
                    DataTable(
                        id='table-precios',
                        columns=[
                            {
                                'name': 'Sede',
                                'id': 'sede',
                                'deletable': False,
                                'renamable': False,
                            },
                            {
                                'name': 'Material',
                                'id': 'material',
                                'deletable': False,
                                'renamable': False,
                            },
                            {
                                'name': '  Precio RA',
                                'id': 'preciora',
                                'deletable': False,
                                'renamable': False,
                                "type": 'numeric',
                                "format": FormatTemplate.money(2)
                            },
                            {
                                'name': '  Precio LE',
                                'id': 'preciole',
                                'deletable': False,
                                'renamable': False,
                                "type": 'numeric',
                                "format": FormatTemplate.money(2)
                            }
                        ],
                        data=[
                            {"material": ""
                                , "precioventa": "",
                             "preciocompra": "",
                             "sede": ""}
                        ],
                        editable=True,
                        row_deletable=True,
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
                        style_cell_conditional=[
                            {'if': {'column_id': 'sede'},
                             'width': '150px'},
                            {'if': {'column_id': 'material'},
                             'width': '150px'},
                            {'if': {'column_id': 'preciora'},
                             'width': '100px'},
                            {'if': {'column_id': 'preciole'},
                             'width': '100px'},
                            {'if': {'column_id': ''},
                             'width': '25em'},
                        ]

                    ),
                ],
                id="table-precios-div"
            ),

            html.Div(
                children=[  # ButtonGroup de la tabla
                    html.Div([
                        dbc.Button(
                            children=[
                                dcc.Upload(
                                    children=[
                                        html.Img(
                                            src=app.get_asset_url("upload.svg"),
                                            id="cargar-img"
                                        ),
                                        html.P(
                                            "Cargar\nArchivo",
                                            id="cargar-text"
                                        ),
                                    ],
                                    id="upload-comp"
                                ),
                            ],
                            id="button-load-file",
                            n_clicks=0,
                            className="mr-1 mt-1 btn btn-primary buttons-table start-button"
                        ),

                        dbc.Button(
                            children=[
                                html.Img(
                                    src=app.get_asset_url("download.svg")),
                                html.P("Guardar\nArchivo")
                            ],
                            id="button-save-file",
                            n_clicks=0,
                            className="mr-1 mt-1 btn btn-primary buttons-table mid-button"
                        ),

                        dbc.Button(
                            children=[
                                html.Img(
                                    src=app.get_asset_url("add.svg")),
                                html.P("Agregar\nMaterial")
                            ],
                            id="button-add-row",
                            n_clicks=0,
                            className="mr-1 mt-1 btn btn-primary buttons-table end-button"
                        ),
                    ],
                        id="button-add-row-div"
                    )
                ],
                id="container-buttons"
            ),

        ],
    ),

    # Tabs ----------------------------------------------------------------------------------------------------------------------------

    html.Div(
        children=[
            dcc.Tabs(  # Almacena las dos tabs adentro
                id="tabs-finanzas",

                children=[
                    dcc.Tab(  # Tab Individual
                        children=[
                            html.Div(  # Contenedor de la informacion del Tab
                                children=[
                                    html.Div([
                                        html.Img(
                                            src=app.get_asset_url("wave.png"),
                                            className="waves"
                                        ),

                                        dcc.Input(
                                            id="input-legacyId",
                                            placeholder="Numero de Legajo",
                                            style={
                                                "display": "block"
                                            },
                                            autoComplete="off"
                                        ),
                                    CreateButton("search-button","Buscar")
                                    ],
                                        id="search-div",
                                        className=""  # Contenedor de la parte de busqueda
                                    ),

                                    html.Div(
                                        children=[
                                            dbc.Spinner(
                                                id="loading",
                                                children=[
                                                    html.Div([
                                                        html.P(
                                                            "Total",
                                                            id="label-total"
                                                        ),

                                                        cards_individual,
                                                    ],
                                                    ),
                                                ],
                                                color="primary",
                                                debounce="10",
                                                spinner_style={
                                                    "width": "5rem",
                                                    "height": "5rem",
                                                    "z-index": "2",
                                                    "display": "absolute",
                                                    "top": "20rem"
                                                },

                                            ),
                                        ],
                                        id="div-individual"  # Contenedor del retorno (Graficos y metricas)
                                    ),
                                ],
                            ),
                        ],
                        id="tab1-finanzas",
                        className="tabs tab-finanzas-header tab",
                        label="Individual",
                        value="individual"
                    ),

                    dcc.Tab(  # Tab Todxs
                        label="Todxs",
                        value="todxs",
                        children=[
                            html.Div(  # Contenedor de la info del Tab
                                children=[
                                    html.Button(  # Boton de refrescar
                                        children=[
                                            html.Img(
                                                src=app.get_asset_url("renew.svg"),
                                                id="img-refresh"
                                            ),

                                            html.P(
                                                "Refrescar",
                                                style={
                                                    "display": "inline-block",
                                                    "fontSize": "20px",
                                                    "fontFamily": "Rubik,sans",
                                                    "marginTop": "-2px"
                                                },
                                            ),
                                        ],
                                        id="refresh-button",
                                        className="mr-1 mt-1 btn btn-primary"
                                    ),

                                    dbc.Spinner(
                                        children=[
                                            html.P(
                                                "Si no ves nada acá presioná el botón de Refrescar",
                                                id="parent-todxs"
                                            ),
                                        ],
                                        size="md",
                                        fullscreen=False,
                                        id="loading-2",
                                    ),
                                ],
                                style={
                                    "position": "relative",
                                    "top": 0,
                                    "bottom": 0,
                                    "weight": "100%",
                                    "margin": "0 auto",
                                    "padding": "0 auto"
                                },
                            ),
                        ],
                        id="tab2-finanzas",
                        className="tabs tab-finanzas-header tab",
                    ),
                ],
                value="individual"
            ),
        ],
        style={
            "width": "60%",
            "display": "inline-block",
            "float": "right"
        },
    ),
    

])

"""
----------------------------------------------------------------------------------------------------------------------------------------------

Callbacks

----------------------------------------------------------------------------------------------------------------------------------------------

"""


@app.callback(
    Output('table-precios', 'data'),
    Output("download", "data"),
    Output("tabla-error-modal", "is_open"),
    Input('button-save-file', 'n_clicks'),
    # Input("button-load-file","n_clicks"),
    Input('button-add-row', 'n_clicks'),
    Input('upload-comp', 'contents'),
    Input("close-modal-data-table-button", "n_clicks"),
    State('table-precios', 'data'),
    State('table-precios', 'columns'),
    State('upload-comp', 'filename'), )
def add_row(n_clicks_save, n_clicks_add, content, close_n_clicks, rows, columns, filename):
    """
    Funcion que controla la carga, descarga e información de la tabla. Llama al trigger para chequear
    de donde viene el callback y con ese ejecuta la logica correspondiente.
    """

    trigger = callback_context.triggered[0]
    print(trigger)
    if trigger["prop_id"] == "button-add-row.n_clicks":
        if n_clicks_add > 0:
            if rows == None:
                rows = [({c['id']: '' for c in columns})]
            else:
                rows.append(({c['id']: '' for c in columns}))
        return rows, None, False

    elif trigger["prop_id"] == "button-save-file.n_clicks":
        df_file = pd.DataFrame(rows).to_csv(index=False)
        return rows, dict(content=df_file, filename="Precios.csv"), False

    elif trigger["prop_id"] == "upload-comp.contents":
        if content is not None:
            try:
                df = utils_finanzas.parse_contents(content, filename)
                if not df.empty:
                    df_table = [df.iloc[i].to_dict() for i in range(len(df.index))]
                    return df_table, None, False
                else:
                    return rows, None, True
            except:
                return rows, None, True
        else:
            return rows, None, True
    elif trigger["prop_id"] == "close-modal-data-table-button.n_clicks":
        return rows, None, False
    else:
        return rows, None, False


@app.callback(
    [
        Output("label-total", "children"),
        Output("sininfo-modal", "is_open"),
        Output("parent-todxs", "children")
    ],
    [
        Input("search-button", "n_clicks"),
        Input("close-modal-sin-info-button", "n_clicks"),
        Input("tabs-finanzas", "value"),
        Input("refresh-button", "n_clicks"),
        State("dropdown-predios", "value"),
        State("date-range-finanzas", "start_date"),
        State("date-range-finanzas", "end_date"),
        State("input-legacyId", "value"),
        State("table-precios", "data"),
        State("sininfo-modal", "is_open"),
        State("radio-button-fechas", "value")
    ]
)
def filtrar_rutas(n_clicks, close_n_clicks, tab, refresh_n_clicks, predios, fecha_inicio, fecha_fin, legacy_id, data,
                  sininfo_is_open, radio_button_val):
    """
    Funcion que controla el filtrado de la informacion y devuelve los graficos y metricas correspondientes de la parte de finanzas.
    Llama al trigger para ver de donde viene la señal y segun eso ejecuta un proceso distinto.
    """

    df = MTEDataFrame.get_instance()
    trigger = callback_context.triggered[0]

    if trigger["prop_id"] == "search-button.n_clicks":
        if n_clicks > 0:
            df_filtrado = utils_finanzas.crear_df_filtrado(df, [predios], datetime.fromisoformat(fecha_inicio),
                                                           datetime.fromisoformat(fecha_fin), [], [])
            if df_filtrado.empty:
                sininfo_is_open = not sininfo_is_open

    elif tab == "todxs":
        df_filtrado = utils_finanzas.crear_df_filtrado(df, [predios], datetime.fromisoformat(fecha_inicio),
                                                       datetime.fromisoformat(fecha_fin), [], [])
        if df_filtrado.empty:
            sininfo_is_open = not sininfo_is_open

    elif trigger["prop_id"] == "refresh-button.n_clicks":
        df_filtrado = utils_finanzas.crear_df_filtrado(df, [predios], datetime.fromisoformat(fecha_inicio),
                                                       datetime.fromisoformat(fecha_fin), [], [])
        if df_filtrado.empty:
            sininfo_is_open = not sininfo_is_open

    elif trigger["prop_id"] == "close-modal-sin-info-button.n_clicks":
        sininfo_is_open = not sininfo_is_open

    return [n_clicks, sininfo_is_open, n_clicks]
