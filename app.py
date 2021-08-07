from datetime import date, datetime
import dash
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
from dash.dependencies import Output, Input
# from future.utils import ensure_new_type

import plotly.graph_objects as go

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)

app.title = "Tablero MTE"
# Para que no tire error al principio por las callbacks cruzadas
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.Div(id="div-izquierda", children=[
        html.Img(
            src=app.get_asset_url("logo_negro.png"), className="logo-mte"
        ),
        html.Label("Elegí el rango de fechas"),
        dcc.DatePickerRange(
            id="date-range",
            display_format="D/M/Y",
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2021, 12, 31),
            start_date=date(2019, 5, 15),
            end_date=date(2020, 10, 20),
        ),
        html.Label("Elegí el predio"),
        dcc.Dropdown(
            id="dropdown-predio",
            options=[
                dict(label="Avellaneda", value="AVELLANEDA"),
                dict(label="Barracas", value="BARRACAS"),
                dict(label="Cortejarena", value="CORTEJARENA"),
                dict(label="Saavedra", value="SAAVEDRA"),
                dict(label="No especificado", value="No especificado"),
            ], 
            value="SAAVEDRA",
            # multi=True  # Por ahora lo apago para que funcione la versión preliminar pero después lo necesitamos
        )
    ], style={"display": "inline-block", "width": "30%"}),
    html.Div([
    dcc.Tabs(id="tabs",
        children=[
            dcc.Tab(label="Pestaña 1", value="tab_1"),
            dcc.Tab(label="Pestaña 2", value="tab_2"),
        ],
        value="tab_1"
    ),
    html.Div(id="salida-tabs"),
    html.H1("hola"),
    ], style={"width": "70%", "display": "inline-block", "float": "right"}
    ),

])

#Preproceso 
import pandas as pd
import plotly.express as px
dtypes = {'etapa': str, 'bolson': float, 'camion': str, 'peso': int, 'cartonero': str, 'legacyId': str, 'predio': str, 'material': str}
df = pd.read_csv("data/pesajes-01-01-2019-31-12-2020_anonimizado.csv", dtype=dtypes, parse_dates=[0])

df_preprocesado = df.copy()
df_preprocesado['predio'] = df_preprocesado['predio'].fillna('No especificado')
df_preprocesado['material'] = df_preprocesado['material'].fillna('No especificado')

df_predio = df_preprocesado.groupby(['fecha','predio'])['peso'].sum().reset_index()

#Funcion 
def graficar_material_predio(fecha_inicio, fecha_fin, predio, mode):
  condicion_temporal = (df_predio['fecha'] >= fecha_inicio) & (df_predio['fecha'] <= fecha_fin)
  condicion_predio = df_predio['predio'] == predio
  condicion = condicion_temporal & condicion_predio
  df_graficar = df_predio[condicion]
  traces = [
      go.Scatter({"x": df_graficar.fecha, "y": df_graficar.peso}, mode=mode),    
  ]
  layout = {
      "title": "titulo",
      "xaxis": dict(title="eje x"),
  }
  figure = dict(data=traces, layout=layout)

  return figure


@app.callback(
    Output("salida-tabs", "children"),
    Input("tabs", "value")
)
def render_content(value):
    if value == "tab_1":
        return [html.H1("esta es la tab 1"),
                html.Label("Elegí el tipo de gráfico"),
                dcc.Dropdown(id="dropdown",
                    options=[
                        dict(label="Línea", value="lines"),
                        dict(label="Dispersión", value="markers"),
                        dict(label="Línea + Dispersión", value="markers+lines"),
                    ],
                    value="markers+lines"
                ),
                dcc.Graph(id="graph_1")
        ]
    else:
        return html.H1("esta es la tab 2")


@app.callback(
    Output("graph_1", "figure"),
    Input("dropdown", "value"),
    Input("dropdown-predio", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_graph(mode, predio, start_date, end_date):
    print("DEBUG: se ejecutó update_graph")
    # print("START:", start_date, type(start_date))
    figure_1 = graficar_material_predio(datetime.fromisoformat(start_date), datetime.fromisoformat(end_date), predio, mode)
    return figure_1


if __name__ == "__main__":
    app.run_server(debug=True, port=5050)

"""
Crash course de plotly.Figure.
La estructura básica es
figure = {
    "data": [lista (si o si) con la o las traces del estilo go.Scatter()],
    "layout" : {
        "title": "titulo del grafico",
        "xaxis": {
            "title": "eje x"
        }
    }
}
Un lindo quilombo de diccionarios anidados.

Esto se puede reemplazar por directamente gráficos de plotly.express que devuelven figuras

figure = px.line()

O sino tmb con los objetos de plotly.graph_objecs

figure = go.Figure(
    data=[go.Scatter],
    layout=go.Layout(
        propiedades=blabla
    )
)
estos no los usé mucho sinceramente

Les dejo las documentaciones para chusmear

https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html
https://plotly.com/python/reference/layout/
"""