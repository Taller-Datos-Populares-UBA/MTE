import base64
import io

import dash_html_components as html
import pandas as pd
import plotly.express as px

from elements import EmptyFigure


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        df = None
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        return df
    except Exception as e:
        return html.Div([
            'There was an error processing this file.'
        ])


def grafico_torta(legajo, df):
    df_cartoneros = df.groupby(by=["cartonero", "material", "legacyId"], ).sum()[["peso"]]
    df_cartoneros.reset_index(inplace=True)
    df_aux = df_cartoneros.loc[df_cartoneros["legacyId"] == str(legajo)]

    if df_aux.empty:
        return EmptyFigure()

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


def retornar_df_pagos(df_filtrado, df_precios):
    df_pagos = df_filtrado.copy()
    df_pagos["precio/kg"] = 0
    df_pagos["precio"] = 0
    for index, row in df_precios.iterrows():
        sede = row["sede"]
        material = row["material"]

        indices_LE = df_pagos[(df_pagos["predio"] == sede) & (df_pagos["material"] == material) & (
                df_pagos["tipoCartonero"] == "LE")].index
        indices_RA = df_pagos[(df_pagos["predio"] == sede) & (df_pagos["material"] == material) & (
                df_pagos["tipoCartonero"] == "RA")].index

        precio_LE = row["preciole"]
        precio_RA = row["preciora"]
        df_pagos.loc[indices_LE, "precio/kg"] = precio_LE
        df_pagos.loc[indices_RA, "precio/kg"] = precio_RA

    df_pagos["precio"] = df_pagos["precio/kg"] * df_pagos["peso"]
    return df_pagos


def pago_por_predio(df_filtrado, df_precios):
    df_pagos = retornar_df_pagos(df_filtrado, df_precios)
    df_pagos = df_pagos.groupby(['predio']).sum('precio')
    return df_pagos[['precio']]


def pago_individual(df_filtrado, df_precios, legajo):
    df_pagos = retornar_df_pagos(df_filtrado, df_precios)
    df_pagos = df_pagos.groupby(['legacyId']).sum('precio')
    pago_ind = df_pagos.loc[legajo]
    return pago_ind['precio']  # En realidad la columna 'precio' es 'pago'.
