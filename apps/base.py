from datetime import date, timedelta

import dash_bootstrap_components as dbc
from dash import callback_context
from dash.dependencies import Output, Input

from app import app
from mte_dataframe import MTEDataFrame

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

@app.callback(
    [
        Output("date-range", "start_date"),
        Output("date-range", "end_date"),
        Output("radio-button-fechas", "value")
    ],
    [
        Input("radio-button-fechas", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ]
)
def cambiar_fecha_calendario(periodo, start_date, end_date):
    trigger = callback_context.triggered[0]

    if trigger["prop_id"] == "date-range.start_date" or trigger["prop_id"] == "date-range.end_date":
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
