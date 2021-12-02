import datetime
import base64
import io

import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


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

    if df_aux.empty:
        fig = go.Figure()

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=10,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0,
                xanchor="center",
                x=0.5
            ),
        ),
        fig.update_xaxes(
            zeroline=False,
            showgrid=False,
            tickmode="array",
            tickvals=[],
            ticktext=[]
        )
        fig.update_yaxes(
            zeroline=False,
            showgrid=False,
            tickmode="array",
            tickvals=[],
            ticktext=[]
            )
    else:
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


# def calcular_pago(df, legajo, df_precio):
#     """recibe df filtrado.
#     creo que hay q borrarla esta funcion!"""
#     df_legajo = df[df['legacyId'] == legajo]
#     df_legajo_materiales = df_legajo.groupby(['material'])['peso'].sum().reset_index()
#     costo_neto = 0
#     try:
#         for index, row in df_legajo_materiales.iterrows():
#             costo_material = df_precio[df_precio['material'] == 'Mezcla B']['preciora'].values[0] * row['peso']
#             costo_neto += costo_material
#     except IndexError:
#         costo_neto="Error"

#     return costo_neto, df_legajo


def retornar_df_pagos(df_filtrado, df_precios):
    df_pagos = df_filtrado.copy()
    df_pagos["precio/kg"] = 0
    df_pagos["precio"] = 0
    for index, row in df_precios.iterrows():
        sede = row["sede"]
        material = row["material"]

        indices_LE = df_pagos[(df_pagos["predio"] == sede) & (df_pagos["material"] == material) & (df_pagos["tipoCartonero"] == "LE")].index
        indices_RA = df_pagos[(df_pagos["predio"] == sede) & (df_pagos["material"] == material) & (df_pagos["tipoCartonero"] == "RA")].index

        precio_LE = row["preciole"]
        precio_RA = row["preciora"]
        df_pagos.loc[indices_LE, "precio/kg"] = precio_LE
        df_pagos.loc[indices_RA, "precio/kg"] = precio_RA

    df_pagos["precio"] = df_pagos["precio/kg"]*df_pagos["peso"]
    return df_pagos


def pago_por_compa(df_filtrado, df_precios):
    df_pagos = retornar_df_pagos(df_filtrado, df_precios)
    df_pagos = df_pagos.groupby(['predio']).sum('precio')
    return df_pagos[['precio']]


def pago_individual(df_pagos, legajo):
    return df_pagos.loc[legajo]
