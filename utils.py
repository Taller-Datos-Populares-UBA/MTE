import pandas as pd

import plotly.express as px


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
#   df_filtrado = df_filtrado.fillna('No especificado')  # ya lo hicimos arriba

  #crear columna de tipos de cartoneres
  df_filtrado['tipoCartonero'] = df_filtrado.apply(determinar_tipo_cartonero, axis=1)

  #aplicar filtros
  df_filtrado = df_filtrado.loc[df_filtrado['predio'].isin(predios)]
  df_filtrado = df_filtrado[(df_filtrado['fecha'] >= fecha_inicio)&(df_filtrado['fecha'] <= fecha_finalizacion)]
  df_filtrado = df_filtrado.loc[df_filtrado['material'].isin(materiales)]
  df_filtrado = df_filtrado.loc[df_filtrado['tipoCartonero'].isin(tipoCartonero)]

  return df_filtrado


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


dtypes = {'etapa': str, 'bolson': float, 'camion': str, 'peso': int, 'cartonero': str, 'legacyId': str, 'predio': str, 'material': str}

df_1 = pd.read_csv("data/pesajes-01-01-2019-31-12-2020_anonimizado.csv", dtype=dtypes, parse_dates=[0])
df_2 = pd.read_csv("data/pesajes-30-07-2021-06-08-2021_anonimizado.csv", dtype=dtypes, parse_dates=[0])

df = pd.concat([df_1,df_2], ignore_index=True)
df['fecha'] = pd.to_datetime(df['fecha'])
df = df.fillna('No especificado')


predios = df.predio.unique()


rutas = [
    'R8', 'R16', 'R12', 'E2C', 'E1', 'E2B', 'RIS', 'E5', 'E10', 'EVU',
    'E13', 'Avellaneda (A)', 'Avellaneda (C)', 'Avellaneda (D)',
    'Avellaneda (F)', 'Avellaneda (E)', 'Avellaneda (B)', 'R1', 'R5',
    'R11', 'E8C', 'R14', 'R26', 'R22', 'R25', 'R3', 'E8A ', 'E8B',
    'R6', 'R7', 'R9', 'R15', 'R17', 'R20', 'R21', 'R24', 'E2A',
]

materiales = df.material.unique()