from datetime import date, datetime, timedelta

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash import callback_context
from dash.dependencies import Output, Input, State
from dash_table import DataTable, FormatTemplate

from utils.utils import crear_df_filtrado
from utils.utils_finanzas import grafico_torta, parse_contents  # , calcular_pago
from utils.utils_finanzas import pago_por_compa, pago_individual

from app import app
from mte_dataframe import MTEDataFrame

from elements import CreateButton, SelectDates, SelectFilterOptions, CreateModal

# Carga de DataFrames
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


# EMPROLIJAR
import plotly.graph_objs as go
fig = go.Figure()
# fig = grafico_torta("NA", df)  # Creo una figura vacia rellenar la card que lleva el grafico

#--------------------------------------------------------------------------------------------------------------------------

# Cards

#--------------------------------------------------------------------------------------------------------------------------

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
            ])
        ], id="tabla-legajo-parent")],
    className="card last-card",
)

# Card con el grafico
third_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Material recolectado", className="card-title"),
            dcc.Graph(id="graph-legajo", figure=fig, config={'displaylogo': False, 'displayModeBar': False, 'locale': 'es'}),
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
                        dbc.Col(html.Div(id="warning-subir-archivo-finanzas"),),
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

    CreateModal("legacy_id", "No se encontró el número de legajo", "Revisá si está correctamente colocado el número de legajo."),

    CreateModal("archivoerror", "Problemas con el archivo", "El archivo parece estar dañado, vacio, o con un formato no soportado."),


    dcc.Download(id="download"),

    # Filtros ------------------------------------------------------------------------------------------------------------------------

    html.Div(
        id="botonera",
        className="botonera",
        children=[

            html.H6(  # Titulo Botonera
                "Filtros",
                className="title-botonera"
            ),

            html.Div(
                children=[  # Radiobuttons y picker de fechas
                    SelectDates("date-range-finanzas", "radio-button-fechas-finanzas"),
                    SelectFilterOptions(predios, "Elegí el predio", "dropdown-predios", "salida-predios", capitalize=True),
                    ]
            ),
            SelectFilterOptions(rutas, "Elegí la ruta", "dropdown-rutas", "salida-rutas", add_all_as_option=True, capitalize=True),

            SelectFilterOptions(cartoneres, "Elegí el tipo de cartonere", "dropdown-cartonerx", "salida-cartoneres"),

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
                                        DataTable(
                                            id="df_pagos",
                                            columns=[{"name": "Legajo", "id": "legacyId"},
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
                                                "height": "200px",
                                                "minHeight": "200px",
                                                "maxHeight": "700px",
                                                "overflowX": "auto"
                                            },
                                            fixed_rows={'headers': True},

                                        )],
                                        id="df-precios-parent"),

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
                                    )],

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


# Funcion que controla los radiobuttons de las fechas y la fecha que aparece en el calendario
@app.callback(
    [
        Output("date-range-finanzas", "start_date"),
        Output("date-range-finanzas", "end_date"),
        Output("radio-button-fechas-finanzas", "value")
    ],
    [
        Input("radio-button-fechas-finanzas", "value"),
        Input("date-range-finanzas", "start_date"),
        Input("date-range-finanzas", "end_date"),
    ]
)
def cambiarFechaCalendario(periodo, start_date, end_date):
    trigger = callback_context.triggered[0]

    # Si llamo a la función desde los input de las fechas se tendria que cambiar a otro automaticamente el periodo
    if trigger["prop_id"] == "date-range-finanzas.start_date" or trigger["prop_id"] == "date-range-finanzas.end_date":
        fecha_inicio = start_date
        fecha_finalizacion = end_date
        periodo = "otro"

    # Si no viene de los input, viene de los radiobutton.
    # Luego que modifique la fecha de los input con la opcion del radiobutton que llega
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


# Función que controla todo lo que muestra en la parte de Individual y Todxs
@app.callback(
    [
        Output("label-total", "children"),
        Output("sininfo-modal", "is_open"),
        Output("parent-todxs", "children"),
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
        State("date-range-finanzas", "start_date"),
        State("date-range-finanzas", "end_date"),
        State("input-legacyId", "value"),
        State("table-precios", "data"),
        State("sininfo-modal", "is_open"),
        State("graph-legajo", "figure"),
        State("label-legajo", "children"),
        State("legacy_id-modal", "is_open"),
        State("tabla-legajo", "data"),
        State("errorpago-modal", "is_open")
    ],
    prevent_initial_call=True
)
def filtrar_rutas(n_clicks, close_n_clicks, close_n_clicks_2, close_n_clicks_3, tab, refresh_n_clicks, predios, fecha_inicio, fecha_fin, legacy_id, data,
                  sininfo_is_open, figure, pago, legacy_id_no_encontrado_is_open, ultimos_movimientos, errorpago_is_open):
    df = MTEDataFrame.get_instance()
    trigger = callback_context.triggered[0]
    df_pagos=pd.DataFrame()
    # Si llame a la funcion apretando el boton de refrescar, buscar, o cambie a la tab de Todxs:
    if trigger["prop_id"] in ["refresh-button.n_clicks"] and tab == "todxs":
        df_precios = pd.DataFrame(data)
        df_filtrado = crear_df_filtrado(df, predios, datetime.fromisoformat(fecha_inicio),
                                        datetime.fromisoformat(fecha_fin), [], [])
        try:
            df_pagos = pago_por_compa(df_filtrado, df_precios)
        except Exception as e:
            print("No pude calcular el pago, error:", e)

    elif trigger["prop_id"] in ["search-button.n_clicks"]:
        # Solo en este caso va a buscar el df, filtrar, y realizar todos estos procesos que llevan tiempo.
        df_precios = pd.DataFrame(data)
        df_filtrado = crear_df_filtrado(df, predios, datetime.fromisoformat(fecha_inicio),
                                        datetime.fromisoformat(fecha_fin), [], [])

        # Chequea que el df_filtrado no este vacio, y que la persona que buscamos este en el df.
        cond1 = not df_filtrado.empty
        cond2 = legacy_id in list(df_filtrado["legacyId"])

        if cond1 and cond2:  # Si se cumplen las dos condiciones, muestra todo lo que tiene que mostrar

            if trigger["prop_id"] == "search-button.n_clicks":
                figure = grafico_torta(legacy_id, df_filtrado)
                # pago, ultimos_movimientos = calcular_pago(df_filtrado, legacy_id, df_precios)
                try:
                    df_pagos = pago_por_compa(df_filtrado, df_precios)
                    pago = pago_individual(df_pagos, legacy_id)[0]
                except Exception as e:
                    print("No pude calcular el pago, error:", e)
                ultimos_movimientos = df_filtrado[df_filtrado.legacyId==legacy_id]
                if pago=="Error":  # Del hecho de que la tabla de precios esta vacio
                    errorpago_is_open = not errorpago_is_open
                else:  # Modificamos el formato del pago
                    pago="$ "+str(pago)

                ultimos_movimientos = ultimos_movimientos.sort_values("fecha", ascending=False)

                if len(ultimos_movimientos.index)>10:
                    ultimos_movimientos = ultimos_movimientos.head(10)
                    ultimos_movimientos["fecha"] = [fecha.isoformat()[:-9] for fecha in ultimos_movimientos.fecha]
                ultimos_movimientos = [ultimos_movimientos.iloc[i].to_dict() for i in range(len(ultimos_movimientos.index))]

        elif not cond1:  # Si el df esta vacio, te avisa con el modal de que esta vacio
            sininfo_is_open = not sininfo_is_open

        elif not cond2:  # Si la persona no esta en el df, te avisa con el modal
            legacy_id_no_encontrado_is_open = not legacy_id_no_encontrado_is_open

    # Los siguientes 3 elif son para cerrar los modals
    elif trigger["prop_id"] == "close-modal-sininfo-button.n_clicks":
        sininfo_is_open = not sininfo_is_open

    elif trigger["prop_id"] == "close-modal-legacy_id-button.n_clicks":
        legacy_id_no_encontrado_is_open = not legacy_id_no_encontrado_is_open

    elif trigger["prop_id"] == "close-modal-errorpago-button.n_clicks":
        errorpago_is_open = not errorpago_is_open
    # print(df_pagos)
    df_pagos=df_pagos.reset_index().to_dict('records')

    return [n_clicks, sininfo_is_open, n_clicks, figure, pago, legacy_id_no_encontrado_is_open, ultimos_movimientos, errorpago_is_open, df_pagos]


@app.callback(
    Output("warning-subir-archivo-finanzas", "children"),
    Input("search-button", "n_clicks")
)
def warning_subir_archivo(n_clicks):
    """
    Agrega un warning si el usuario no cargó un archivo.
    """
    if n_clicks:
        if MTEDataFrame.FILES_TO_LOAD:
            return None
    if MTEDataFrame.FILES_TO_LOAD is None:
        return dbc.Alert("Por favor subir un archivo primero y luego apretar BUSCAR", color="danger", style={"font-size": "20px"})
