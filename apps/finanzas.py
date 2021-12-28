from datetime import datetime

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import State
from dash_table import DataTable, FormatTemplate

from apps.base import *
from elements import CreateButton, CreateModal, CreateFilters
from utils.utils import crear_df_filtrado
from utils.utils_finanzas import grafico_torta, parse_contents
from utils.utils_finanzas import pago_por_predio, pago_individual

from dashfinanzashandler import DashFinanzasHandler

fig = go.Figure()

# --------------------------------------------------------------------------------------------------------------------------

# Cards

tabla_todos = DataTable(
                id="df_pagos",
                columns=[{"name": "Predio", "id": "predio"},
                            {"name": "Pago", "id": "precio"}
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
                    "height": "800px",
                    "minHeight": "200px",
                    "maxHeight": "700px",
                    "overflowX": "auto"
                },
                fixed_rows={'headers': True},

            )

tabla_resumen = DataTable(
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
                    style_cell={
                        "overflowX": "hidden",
                        "textOverflow": "ellipsis",
                        "border": "1px solid black",
                        "border-left": "2px solid black"
                    },
                    style_header={
                        "backgroundColor": "#4582ec",
                        "color": "white",
                        "border": "0px solid #2c559c",
                    },
                )

# --------------------------------------------------------------------------------------------------------------------------

# Card con el saldo
first_card = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Monto a pagar", id="monto-card-saldo", className="card-title"),
            html.P(id="label-legajo"),
        ]
    )]
)

# Card con la tabla de ultimos movimientos
second_card = dbc.Card([
    dbc.CardBody(
        [
            html.H6("Ultimas cargas", className="card-title"),
            html.Div(children=[
                tabla_resumen
            ])
        ], id="tabla-legajo-parent")],
    className="card last-card",
)

# Card con el grafico
third_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Material recolectado", className="card-title"),
            dcc.Graph(id="graph-legajo", figure=fig,
                      config={'displaylogo': False, 'displayModeBar': False, 'locale': 'es'}),
        ]),
    className="card"
)

# Estructura que almacena todas las cards
cards_individual = html.Div(
    [
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Col(html.Div(id="warning-subir-archivo-finanzas"), ),
                        dbc.Col(
                            first_card,
                        ),
                        dbc.Col(
                            third_card,
                        ),
                        dbc.Col(
                            second_card
                        )
                    ],
                    width=12
                ),
            ],
            id="ro1"
        ),
    ], className="container-cards"
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

    CreateModal("sininfo", "No se encontró información", "Revisá si estan correctamente seleccionados los filtros."),

    CreateModal("errorpago", "Faltan precios", "Revisá si está completa la tabla de precios."),

    CreateModal("legacy_id", "No se encontró el número de legajo",
                "Revisá si está correctamente colocado el número de legajo."),

    CreateModal("archivoerror", "Problemas con el archivo",
                "El archivo parece estar dañado, vacio, o con un formato no soportado."),

    dcc.Download(id="download"),

    # Filtros ------------------------------------------------------------------------------------------------------------------------

    html.Div(
        id="botonera",
        className="botonera",
        children=[
            CreateFilters(predios, rutas, materiales, cartoneres),
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
                    dcc.Store(
                        id="store-precios",
                        storage_type="local"
                    ),
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
                            {"material": "", "preciora": "",
                             "preciole": "",
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
        className="output",
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
                                        CreateButton("search-button", "Buscar"),
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
                                    html.Div(children=[
                                        tabla_todos],
                                        id="df-precios-parent"),
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


# Funcion que controla todos los botones de la tabla de precios
@app.callback(
    Output('table-precios', 'data'),
    Output("download", "data"),
    Output("archivoerror-modal", "is_open"),
    Output("store-precios", "data"),
    Input('button-save-file', 'n_clicks'),
    Input('button-add-row', 'n_clicks'),
    Input('upload-comp', 'contents'),
    Input("close-modal-archivoerror-button", "n_clicks"),
    Input("table-precios", "selected_cells"),
    State('table-precios', 'data'),
    State('table-precios', 'columns'),
    State('upload-comp', 'filename'),
    State("store-precios", "data")
)
def add_row(n_clicks_save, n_clicks_add, content, close_n_clicks, selected_cells, rows, columns, filename, store_data):
    trigger = callback_context.triggered[0]

    # Para que se autoguarde la tabla al desplazarse por la misma
    # OJO: no se guarda si no te moviste de la celda que acabas de escribir
    if selected_cells:
        return rows, None, False, rows

    # Si llame a la función del boton de añadir fila toma las filas que ya teniamos, y le agrega una fila nueva.
    # Si no habia ninguna, crea directamente la primer fila
    if trigger["prop_id"] == "button-add-row.n_clicks":
        if n_clicks_add > 0:
            if rows == None:
                rows = [({c['id']: '' for c in columns})]
            else:
                rows.append(({c['id']: '' for c in columns}))
        return rows, None, False, rows

    # Si llame a la funcion del boton de guardar los archivos, Guarda el archivo como un csv ()
    elif trigger["prop_id"] == "button-save-file.n_clicks":
        df_file = pd.DataFrame(rows).to_csv(index=False)
        return rows, dict(content=df_file, filename="Precios.csv"), False, rows

    # Si llame a la funcion del boton de cargar archivo:
    elif trigger["prop_id"] == "upload-comp.contents":
        # Si no ancele la carga de archivo (Que dispara el callback igual):
        if content is not None:
            # Intente parsearlo, y convertirlo a un dataframe, y luego convertirlo en la lista de diccionarios que necesita dash
            try:
                df = parse_contents(content, filename)
                if not df.empty:  # Si el df que parseamos no esta vacio:
                    df_table = [df.iloc[i].to_dict() for i in range(len(df.index))]
                    return df_table, None, False, df_table
                else:  # Sino no hace nada, pero activa el modal que te avisa que el archivo esta mal
                    return rows, None, True, rows
            # Sino, no hace nada, pero activa el modal que te avisa que el archivo esta mal
            except:
                return rows, None, True, rows
        else:  # Si el content esta vacio, te avisa con el modal tambien
            return rows, None, True, rows

    # Si llame a la función del boton del modal, solo cierra el modal y deja el resto igual
    elif trigger["prop_id"] == "close-modal-archivoerror-button.n_clicks":
        return rows, None, False, rows
    else:
        if store_data:
            rows = store_data
        return rows, None, False, rows


# Función

dash_handler_finanzas = DashFinanzasHandler(tabla_resumen.columns, tabla_todos.columns)

# Función que controla todo lo que muestra en la parte de Individual y Todxs
@app.callback(
    [
        Output("sininfo-modal", "is_open"),
        Output("graph-legajo", "figure"),
        Output("label-legajo", "children"),
        Output("legacy_id-modal", "is_open"),
        Output("tabla-legajo", "data"),
        Output("errorpago-modal", "is_open"),
        Output("df_pagos", "data"),

    ],
    [
        Input("search-button", "n_clicks"),
        Input("close-modal-sininfo-button", "n_clicks"),
        Input("close-modal-legacy_id-button", "n_clicks"),
        Input("close-modal-errorpago-button", "n_clicks"),
        Input("tabs-finanzas", "value"),
        Input("refresh-button", "n_clicks"),
        State("dropdown-predios", "value"),
        State("date-range", "start_date"),
        State("date-range", "end_date"),
        State("input-legacyId", "value"),
        State("table-precios", "data"), 
        State("dropdown-rutas", "value"),
        State("dropdown-materiales", "value"),
        State("dropdown-cartonere", "value"),
    ],
    prevent_initial_call=True
)
def filtrar_rutas(n_clicks, close_n_clicks, close_n_clicks_2, close_n_clicks_3, tab, refresh_n_clicks, predios,
                  fecha_inicio, fecha_fin, legacy_id, data, rutas, materiales, cartonere):

    trigger = callback_context.triggered[0]

    return dash_handler_finanzas.filtrar(trigger, tab, refresh_n_clicks, predios, fecha_inicio, fecha_fin, legacy_id, data, rutas, materiales, cartonere)
