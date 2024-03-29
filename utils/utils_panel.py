import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.utils import crear_tabla

def pesos_historico_predios(data, tipo='predio'):
    '''
    Grafica fecha contra peso (promedio o suma total) entregado ese día agrupando según el predio.
    Devuelve la figura de plotly conteniendo el gráfico.
    '''
    if tipo == 'predio':
        tipo2 = 'material'
    else:
        tipo2 = 'predio'
    df = data.groupby(by=["fecha", tipo, tipo2],
                      as_index=False).sum(numeric_only=True)  # Para sacar la info de materiales, sacar "material"
    fig = px.bar(df, x="fecha", y="peso", color=tipo, hover_data=[tipo2])  # "group"
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])  # Ignora fin de semana
    fig.update_layout(bargap=0.01)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
    )
    return fig


def pesos_historico_materiales(data, tipo):
    '''
    Grafica fecha contra peso (promedio o suma total) entregado ese día agrupando según el predio.
    Devuelve la figura de plotly conteniendo el gráfico.
    '''
    df = data.groupby(by=["fecha", tipo], as_index=False).sum()
    fig = px.bar(df, x="fecha", y="peso", color=tipo, barmode="group")
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])  # Ignora fin de semana
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
    )
    return fig


dic_labels_columnas = {'predio': 'Predio',
                       'material': 'Material',
                       'tipoCartonero': 'Tipo de Cartonere'}


def crear_titulos(columnas_resumen):
    try:
        titulos_columnas = {k: dic_labels_columnas[k] for k in columnas_resumen}
    except Exception:
        titulos_columnas = {}
    titulos_columnas["peso"] = "Peso (kg)"
    return titulos_columnas

def crear_tabla_resumen(df, columnas_resumen):
    '''
    Dados un dataframe y unas columnas este función devuelve una tabla para desplegar.
    '''
    try:
        data=df.groupby(by=columnas_resumen).sum(numeric_only=True).reset_index()
        tabla_resumen = crear_tabla(id="tabla-Resumen",
                                    titulos_columnas=crear_titulos(columnas_resumen),
                                    tipos={"peso": "numeric"},
                                    dimensiones=("auto", "200px"),
                                    )
        tabla_resumen.data=data.to_dict("records")
    except ValueError:
        data = df.sum(numeric_only=True)
        tabla_resumen = crear_tabla(id="tabla-Resumen",
                                    titulos_columnas=crear_titulos([]),
                                    tipos={"peso": "numeric"},
                                    dimensiones=("auto", "200px"),
                                    )
        tabla_resumen.data = [data.to_dict()]

    return tabla_resumen

def pesos_historico_promedio(data, tipo='predio'):
    '''
    Prueba. Grafica el "rolling average" (en cada dia muestra el promedio de los últimos 7 dias).
    '''
    df = data.groupby(by=["fecha", tipo], as_index=False).sum(numeric_only=True)

    # recuperamos primera fecha y ultima fecha
    df = df.sort_values(by="fecha")
    df = df[df[tipo].notna()]

    primer_fecha = df["fecha"].iloc[0]
    ultima_fecha = df["fecha"].iloc[-1]
    rango_fechas = pd.date_range(primer_fecha, ultima_fecha, freq="B")  # B de business days

    fig = go.Figure()
    fig.update_layout(xaxis_title="Fecha", yaxis_title="Peso (kilos)")
    for predio in df[tipo].unique():
        df_predio = df.loc[df[tipo] == predio]

        # agrego ceros
        df_predio.set_index(keys="fecha", inplace=True)
        df_predio = df_predio.reindex(rango_fechas, fill_value=0)

        df_predio = df_predio.drop([tipo],axis=1).rolling("10d", min_periods=0).sum()
        df_predio["peso"] = df_predio["peso"] / 10

        fig.add_scatter(x=df_predio.index, y=df_predio['peso'], mode='lines', name=predio)

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
    )

    return fig


def torta(data, tipo='predio'):
    df = data.groupby(by=[tipo], as_index=False).sum(numeric_only=True)
    fig = px.pie(df, values="peso", names=tipo, title='')
    fig.update_traces(hoverinfo="label+percent", textfont_size=14,
                      textinfo="percent", marker=dict(line=dict(color="#FFFFFF", width=0.1)),
                      textposition="auto")
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
    )
    return fig


def datos_tabla(data, tipo='predio'):
    df = data.drop(columns=["bolson"], errors='ignore')
    suma = df.groupby(by=[tipo]).sum(numeric_only=True).reset_index()
    suma.rename(columns={tipo: 'clasificacion'}, inplace=True)
    return suma
