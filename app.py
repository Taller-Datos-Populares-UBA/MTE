from datetime import date, datetime

import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
from dash.dependencies import Output, Input
# from future.utils import ensure_new_type

import plotly.graph_objects as go

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

predios = [
    'BARRACAS', 'SAAVEDRA', 'AVELLANEDA', "No especificado"
]

rutas = [
    'R8', 'R16', 'R12', 'E2C', 'E1', 'E2B', 'RIS', 'E5', 'E10', 'EVU',
    'E13', 'Avellaneda (A)', 'Avellaneda (C)', 'Avellaneda (D)',
    'Avellaneda (F)', 'Avellaneda (E)', 'Avellaneda (B)', 'R1', 'R5',
    'R11', 'E8C', 'R14', 'R26', 'R22', 'R25', 'R3', 'E8A ', 'E8B',
    'R6', 'R7', 'R9', 'R15', 'R17', 'R20', 'R21', 'R24', 'E2A',
]

materiales = [
    'Mezcla B', 'Papel Blanco B', 'Vidrio B', 'Chatarra', 'TELA'
]

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
            end_date=date(2021, 8, 10),
        ),
        html.Label("Elegí el predio"),
        dcc.Dropdown(
            id="dropdown-predios",
            options=[
                {"label": predio.capitalize(), "value": predio} for predio in predios
            ],
            value=predios,
            multi=True  # Por ahora lo apago para que funcione la versión preliminar pero después lo necesitamos
        ),
        html.H6(id="salida-predios"),
        html.Label("Elegí la ruta o etapa"),
        dcc.Dropdown(
            id="dropdown-rutas",
            options=
            [{"label": "Todas", "value": "TODAS"}]+[{"label": ruta.capitalize(), "value": ruta} for ruta in rutas],
            
            multi=True,
            value=["TODAS"],
        ),
        html.H6(id="salida-rutas"),
        html.Label("Elegí el tipo de material"),
        dcc.Dropdown(
            id="dropdown-materiales",
            options=
            [{"label": material.capitalize(), "value": material} for material in materiales],
            
            multi=True,
            value=materiales,
        ),
        html.H6(id="salida-materiales"),
        html.Label("Elegí el tipo de cartonere"),
        dcc.Dropdown(
            id="dropdown-cartonere",
            options=[
                dict(label="LE", value="LE"),
                dict(label="RA", value="RA"),
                dict(label="No especificado", value="No especificado")
            ],
            multi=True,
            value=["LE", "RA", "No especificado"],
        ),


    ], style={"display": "inline-block", "width": "30%"}
    ),
    html.Div([
    dcc.Tabs(id="tabs",
        children=[
            dcc.Tab(label="Pestaña 1", value="tab_1"),
            dcc.Tab(label="Pestaña 2", value="tab_2"),
        ],
        value="tab_1"
    ),
    html.Div(
        id="salida-tabs",
        children=[
            dcc.Graph(id="grafico-historico"),
            dcc.Graph(id="grafico-torta")
        ]
    ),
    ], style={"width": "70%", "display": "inline-block", "float": "right"}
    ),

])

#Preproceso 
# import pandas as pd
# import plotly.express as px
# dtypes = {'etapa': str, 'bolson': float, 'camion': str, 'peso': int, 'cartonero': str, 'legacyId': str, 'predio': str, 'material': str}
# df = pd.read_csv("data/pesajes-01-01-2019-31-12-2020_anonimizado.csv", dtype=dtypes, parse_dates=[0])

# df_preprocesado = df.copy()
# df_preprocesado['predio'] = df_preprocesado['predio'].fillna('No especificado')
# df_preprocesado['material'] = df_preprocesado['material'].fillna('No especificado')

# df_predio = df_preprocesado.groupby(['fecha','predio'])['peso'].sum().reset_index()

# #Funcion 
# def graficar_material_predio(fecha_inicio, fecha_fin, predio, mode):
#   condicion_temporal = (df_predio['fecha'] >= fecha_inicio) & (df_predio['fecha'] <= fecha_fin)
#   condicion_predio = df_predio['predio'] == predio
#   condicion = condicion_temporal & condicion_predio
#   df_graficar = df_predio[condicion]
#   traces = [
#       go.Scatter({"x": df_graficar.fecha, "y": df_graficar.peso}, mode=mode),    
#   ]
#   layout = {
#       "title": "titulo",
#       "xaxis": dict(title="eje x"),
#   }
#   figure = dict(data=traces, layout=layout)

#   return figure


# @app.callback(
#     Output("salida-tabs", "children"),
#     Input("tabs", "value")
# )
# def render_content(value):
#     if value == "tab_1":
#         return [html.H1("esta es la tab 1"),
#                 html.Label("Elegí el tipo de gráfico"),
#                 dcc.Dropdown(id="dropdown",
#                     options=[
#                         dict(label="Línea", value="lines"),
#                         dict(label="Dispersión", value="markers"),
#                         dict(label="Línea + Dispersión", value="markers+lines"),
#                     ],
#                     value="markers+lines"
#                 ),
#                 dcc.Graph(id="graph_1")
#         ]
#     else:
#         return html.H1("esta es la tab 2")


# @app.callback(
#     Output("graph_1", "figure"),
#     Input("dropdown", "value"),
#     Input("dropdown-predios", "value"),
#     Input("date-range", "start_date"),
#     Input("date-range", "end_date"),
# )
# def update_graph(mode, predio, start_date, end_date):
#     print("DEBUG: se ejecutó update_graph")
#     # print("START:", start_date, type(start_date))
#     figure_1 = graficar_material_predio(datetime.fromisoformat(start_date), datetime.fromisoformat(end_date), predio, mode)
#     return figure_1

dtypes = {'etapa': str, 'bolson': float, 'camion': str, 'peso': int, 'cartonero': str, 'legacyId': str, 'predio': str, 'material': str}

df_1 = pd.read_csv("data/pesajes-01-01-2019-31-12-2020_anonimizado.csv", dtype=dtypes, parse_dates=[0])
df_2 = pd.read_csv("data/pesajes-30-07-2021-06-08-2021_anonimizado.csv", dtype=dtypes, parse_dates=[0])

df = pd.concat([df_1,df_2], ignore_index=True)
df['fecha'] = pd.to_datetime(df['fecha'])

#funcion para crear columna de tipo de cartonere
def determinar_tipo_cartonero(row):
    if row['legacyId'].startswith('LE'):
        val = 'LE'
    elif row['legacyId'] == 'No especificado':
        val = 'No especificado'
    else:
        val = 'RA'
    return val

def crear_df_filtrado(df, predios, fecha_inicio, fecha_finalizacion, materiales, tipoCartonero):
  df_filtrado = df.copy()

  #rellenar nans
  df_filtrado = df_filtrado.fillna('No especificado')

  #crear columna de tipos de cartoneres
  df_filtrado['tipoCartonero'] = df_filtrado.apply(determinar_tipo_cartonero, axis=1)

  #aplicar filtros
  df_filtrado = df_filtrado.loc[df_filtrado['predio'].isin(predios)]
  df_filtrado = df_filtrado[(df_filtrado['fecha'] >= fecha_inicio)&(df_filtrado['fecha'] <= fecha_finalizacion)]
  df_filtrado = df_filtrado.loc[df_filtrado['material'].isin(materiales)]
  df_filtrado = df_filtrado.loc[df_filtrado['tipoCartonero'].isin(tipoCartonero)]

  return df_filtrado

# predios = ['CORTEJARENA','SAAVEDRA']
# fecha_inicio = pd.to_datetime('3/11/2020', format='%d/%m/%Y')
# fecha_finalizacion = pd.to_datetime('3/8/2021', format='%d/%m/%Y')
# materiales = ['Mezcla B', 'TELA', 'Vidrio B']
# tipoCartonero = ['LE']


def pesos_historico(data, desde=None, hasta=None, operacion='promedio'):
    '''Grafica los pesos historicos'''
    # data["fecha"] = pd.to_datetime(data["fecha"],format="%Y-%m-%d")
    # if desde is None:
    #     desde = data['fecha'].min()
    # if hasta is None:
    #     hasta = data['fecha'].max()
    # fecha_inicio = pd.to_datetime(desde)
    # fecha_fin = pd.to_datetime(hasta)
    # filtro = ((data['fecha'] >= fecha_inicio) &
    #           (data['fecha'] <= fecha_fin))
    # filtro = ((data['peso'] < 400) & (data['fecha'] > fecha_inicio) &
    #           (data['fecha'] < fecha_fin))
    if operacion == 'promedio':
        df = data.groupby(by=['fecha', 'predio'], ).mean()
    else:
        df = data.groupby(by=['fecha', 'predio'], ).sum()
    df.reset_index(inplace=True)
    fig = px.scatter(df, x="fecha", y="peso", color="predio", size="peso")
    # fig.add_trace(px.line(df, x="fecha", y="peso").data)
    # fig.show()
    return fig


def torta(data, desde=None, hasta=None):
    ''''''
    # data["fecha"] = pd.to_datetime(data["fecha"],format="%Y-%m-%d")
    # if desde is None:
    #     desde = data['fecha'].min()
    # if hasta is None:
    #     hasta = data['fecha'].max()
    # fecha_inicio = pd.to_datetime(desde)
    # fecha_fin = pd.to_datetime(hasta)
    # filtro = ((data['fecha'] >= fecha_inicio) &
    #           (data['fecha'] <= fecha_fin))
    df = data.groupby(by=['material'], ).sum()
    df.reset_index(inplace=True)
    fig = px.pie(df, values='peso', names='material', title='')
    fig.update_traces(hoverinfo="label+percent", textfont_size=14,
                      textinfo="percent", marker=dict(line=dict(color="#FFFFFF",width=0.1)),
                      textposition="auto")
    # fig.show()
    return fig



@app.callback(
    [
        Output("grafico-historico", "figure"),
        Output("grafico-torta", "figure"),
    ],
    [
        Input("dropdown-predios", "value"),
        Input("dropdown-rutas", "value"),
        Input("dropdown-materiales", "value"),
        Input("dropdown-cartonere", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ]
)
def filtrar_rutas(predios, rutas, materiales, cartonere, fecha_inicio, fecha_fin):
    global df
    df_filtrado = crear_df_filtrado(df, predios, datetime.fromisoformat(fecha_inicio), datetime.fromisoformat(fecha_fin), materiales, cartonere)
    print(df_filtrado)
    # print(df_filtrado.dtypes)
    fig_hist = pesos_historico(df_filtrado, operacion="suma")
    fig_torta = torta(df_filtrado)
    return fig_hist, fig_torta




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