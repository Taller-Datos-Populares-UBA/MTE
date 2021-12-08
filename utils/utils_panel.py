import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

#prueba comentario 8/12

def pesos_historico_predios(data, tipo='predio'):
    '''
    Grafica fecha contra peso (promedio o suma total) entregado ese día agrupando según el predio.
    Devuelve la figura de plotly conteniendo el gráfico.
    '''
    if tipo=='predio':
        tipo2='material'
    else:
        tipo2='predio'
    df = data.groupby(by=["fecha", tipo, tipo2], as_index=False).sum()    # Para sacar la info de materiales, sacar "material"
    fig = px.bar(df, x="fecha", y="peso", color=tipo, hover_data=[tipo2])  # "group"
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])    # Ignora fin de semana
    fig.update_layout(bargap=0.01)
    return fig


def pesos_historico_materiales(data, tipo):
    '''
    Grafica fecha contra peso (promedio o suma total) entregado ese día agrupando según el predio.
    Devuelve la figura de plotly conteniendo el gráfico.
    '''
    df = data.groupby(by=["fecha", tipo], as_index=False).sum()
    fig = px.bar(df, x="fecha", y="peso", color=tipo, barmode="group")
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])    # Ignora fin de semana
    return fig


def pesos_historico_promedio(data,tipo='predio'):
    '''
    Prueba. Grafica el "rolling average" (en cada dia muestra el promedio de los últimos 7 dias).
    '''
    df = data.groupby(by=["fecha", tipo], as_index = False).sum()

    #recuperamos primer fecha y ultima fecha
    df= df.sort_values(by="fecha")
    df=df[df[tipo].notna()]

    primer_fecha=df["fecha"].iloc[0]
    ultima_fecha=df["fecha"].iloc[-1]
    rango_fechas=pd.date_range(primer_fecha, ultima_fecha,freq="B") #B de business days


    fig = go.Figure()
    fig.update_layout(xaxis_title="Fecha", yaxis_title="Peso (kilos)")
    for predio in df[tipo].unique():
        df_predio = df.loc[df[tipo] == predio]

        #agrego ceros
        df_predio.set_index(keys="fecha",inplace=True)
        df_predio=df_predio.reindex(rango_fechas, fill_value=0)


        df_predio = df_predio.rolling("10d", min_periods = 0).sum()
        df_predio["peso"] = df_predio["peso"] / 10

        fig.add_scatter(x=df_predio.index, y=df_predio['peso'], mode='lines', name=predio)
    return fig

def torta(data,tipo='predio'):

    #Realiza un gráfico de torta del peso por material.
    #Devuelve la figura de plotly conteniendo el gráfico.

    df = data.groupby(by=[tipo], as_index = False).sum()
    fig = px.pie(df, values="peso", names=tipo, title='')
    fig.update_traces(hoverinfo="label+percent", textfont_size=14,
                      textinfo="percent", marker=dict(line=dict(color="#FFFFFF", width=0.1)),
                      textposition="auto")
    return fig


def datos_tabla(data,tipo='predio'):
    #if tipo=='predio':
    #    tipo2='material'
    #else:
    #    tipo2='predio'

    #df =data.groupby(by=[tipo, tipo2]).sum()
    df=data
    try:
        df = df.drop(columns=["bolson"])
    except:
        pass
    
    
    suma = df.groupby(by=[tipo]).sum()
    suma=suma.reset_index()
    suma.rename(columns={tipo:'clasificacion'},inplace=True)
    #suma_materiales = df.groupby(by=[tipo2]).sum()
    return suma
