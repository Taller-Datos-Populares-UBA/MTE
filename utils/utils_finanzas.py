import datetime
import base64
import io

import dash_html_components as html
import pandas as pd
import plotly.express as px


def determinar_tipo_cartonero(row):
    if row['legacyId'].startswith('LE'):
        return 'LE'
    elif row['legacyId'] == 'No especificado':
        return 'No especificado'
    else:
        return 'RA'

def crear_df_filtrado_old(df, predios, fecha_inicio=datetime.datetime(1,1,1), fecha_finalizacion=datetime.datetime(3000,12,31), materiales=[], tipo_cartonero=[], periodo='otro'):
    df_filtrado = df.copy()

    # rellenar nans
    df_filtrado = df_filtrado.fillna('No especificado')

    # crear columna de tipos de cartoneres
    df_filtrado['tipoCartonero'] = df_filtrado.apply(determinar_tipo_cartonero, axis=1)

    # aplicar filtros
    if predios != []:
        df_filtrado = df_filtrado.loc[df_filtrado['predio'].isin(predios)]


    df_filtrado = df_filtrado[(df_filtrado['fecha'] >= fecha_inicio) & (df_filtrado['fecha'] <= fecha_finalizacion)]
    if materiales != []:
        df_filtrado = df_filtrado.loc[df_filtrado['material'].isin(materiales)]
    if tipo_cartonero != []:
        df_filtrado = df_filtrado.loc[df_filtrado['tipoCartonero'].isin(tipo_cartonero)]

    return df_filtrado

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df


def grafico_torta(legajo, df):
    df_cartoneros = df.groupby(by=["cartonero", "material", "legacyId"], ).sum()[["peso"]]
    df_cartoneros.reset_index(inplace=True)
    df_aux = df_cartoneros.loc[df_cartoneros["legacyId"] == str(legajo)]
    fig = px.pie(df_aux, values='peso', names='material')

    fig.update_traces(
        hovertemplate='<b>%{label}<b><br><br><b>Peso</b>: %{value} Kg<br>')

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0,
            xanchor="center",
            x=0.5
        )
    )
    return fig


def calcular_pago(df, legajo, df_precio):
    """recibe df filtrado"""
    df_legajo = df[df['legacyId'] == legajo]
    df_legajo_materiales = df_legajo.groupby(['material'])['peso'].sum().reset_index()
    costo_neto = 0
    for index, row in df_legajo_materiales.iterrows():
        costo_material = df_precio[df_precio['material'] == 'Mezcla B']['preciocompra'].values[0] * row['peso']
        costo_neto += costo_material
    return costo_neto


def crear_df_filtrado(df, predios, fecha_inicio, fecha_finalizacion, materiales, tipo_cartonero):
    df_filtrado = df.copy()

    # rellenar nans
    df_filtrado = df_filtrado.fillna('No especificado')

    # crear columna de tipos de cartoneres
    df_filtrado['tipoCartonero'] = df_filtrado.apply(determinar_tipo_cartonero, axis=1)

    # aplicar filtros
    if predios:
        df_filtrado = df_filtrado.loc[df_filtrado['predio'].isin(predios)]

    df_filtrado = df_filtrado[(df_filtrado['fecha'] >= fecha_inicio) & (df_filtrado['fecha'] <= fecha_finalizacion)]

    if materiales:
        df_filtrado = df_filtrado.loc[df_filtrado['material'].isin(materiales)]

    if tipo_cartonero:
        df_filtrado = df_filtrado.loc[df_filtrado['tipoCartonero'].isin(tipo_cartonero)]

    return df_filtrado
