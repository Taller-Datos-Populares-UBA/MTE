from datetime import date, timedelta

import dash_bootstrap_components as dbc
from dash import callback_context
from dash.dependencies import Output, Input

from app import app
from mte_dataframe import MTEDataFrame


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
        return dbc.Alert("Por favor subir un archivo primero y luego apretar FILTRAR", color="danger",
                         style={"font-size": "20px"})
