import plotly.express as px
import pandas as pd


def pesos_historico_predios(data, tipo='predio'):
    '''
    Grafica fecha contra peso (promedio o suma total) entregado ese día agrupando según el predio.
    Devuelve la figura de plotly conteniendo el gráfico.
    '''
    if tipo=='predio':
        tipo2='material'
    elif tipo=='material':
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


def pesos_historico_promedio(data):
    '''
    Prueba. Grafica el "rolling average" (en cada dia muestra el promedio de los últimos 7 dias). 
    '''
    df = data.groupby(by=["fecha", "predio"], as_index=False).sum()
    # print(df)

    # recuperamos primer fecha y ultima fecha
    df= df.sort_values(by="fecha")
    df=df[df['predio'].notna()]

    primer_fecha=df["fecha"].iloc[0]
    ultima_fecha=df["fecha"].iloc[-1]
    rango_fechas=pd.date_range(primer_fecha, ultima_fecha, freq="B")  # B de business days

    figures = []
    for predio in df["predio"].unique():
        print(predio)
        df_predio = df.loc[df['predio'] == predio]

        # agrego ceros
        df_predio.set_index(keys="fecha", inplace=True)
        df_predio=df_predio.reindex(rango_fechas, fill_value=0)

        df_predio = df_predio.rolling("10d", min_periods=0).sum()
        df_predio["peso"] = df_predio["peso"] / 10

        #fig = px.line(df_predio, x = "fecha", y = "peso")
        fig = px.line(df_predio, y="peso")
        #fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])
        figures.append(fig)
    return figures[0]

def torta(data):

    # Realiza un gráfico de torta del peso por material.
    # Devuelve la figura de plotly conteniendo el gráfico.

    df = data.groupby(by=["material"], as_index=False).sum()
    fig = px.pie(df, values="peso", names="material", title='')
    fig.update_traces(hoverinfo="label+percent", textfont_size=14,
                      textinfo="percent", marker=dict(line=dict(color="#FFFFFF", width=0.1)),
                      textposition="auto")
    return fig


def datos_tabla(data):
    df =data.groupby(by=["predio", "material"]).sum()
    # print(df.head(10))
    try:
        df = df.drop(columns=["bolson"])
    except:
        pass
    suma_predios = df.groupby(by=["predio"]).sum()
    suma_materiales = df.groupby(by=["material"]).sum()
    return df, suma_predios, suma_materiales



# desde aca, todo es viejo
'''
def pesos_historico(data, operacion='promedio'):
    if operacion == 'promedio':
        df = data.groupby(by=['fecha', 'predio'], ).mean()
    else:
        df = data.groupby(by=['fecha', 'predio'], ).sum()
    df.reset_index(inplace=True)
    fig = px.scatter(df, x="fecha", y="peso", color="predio", size="peso")
    return fig
'''
'''
VIEJA
def pesos_historico_predios(data):
    
    Grafica fecha contra peso (promedio o suma total) entregado ese día agrupando según el predio.
    Devuelve la figura de plotly conteniendo el gráfico.
    
    df = data.groupby(by=["fecha", "predio", "material"], as_index = False).sum()    # Para sacar la info de materiales, sacar "material"
    fig = px.bar(df, x="fecha", y="peso", color="predio", barmode = "group", hover_data=["material"])
    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])])    # Ignora fin de semana

    fig.update_traces(
        hovertemplate ='<br><b>Peso</b>: %{y} Kg<br>',
    ),
    fig.update_layout(
        showlegend=False,
        hovermode="x unified",
        xaxis_tickformat = '%d-%m-%Y',
        yaxis_tickformat = 'digit',
        paper_bgcolor="rgba(0,0,0,0)",
        hoverlabel=dict(bgcolor="white"),

        xaxis=dict(
            zeroline=False,
            showgrid=False,
            showticklabels=True,
            mirror=True,
            ticks="outside",
            tickfont=dict(family="Arial",
                          size=13,
                          color="rgb(0,0,0)",),
            ),

        yaxis=dict(
            showgrid=True,
            zeroline=False,
            mirror=True,
            ticks="outside",
            tickfont=dict(family="Arial",
                          size=13,
                          color="rgb(0,0,0)")),
        xaxis_title=dict(text="Fecha",
                         font=dict(
                             size=15,
                             color="rgb(0,0,0)",)
                        ),
        yaxis_title=dict(text="Kilos (Kg)",
                         font=dict(
                                   size=15,
                                   color="rgb(0,0,0)",)),
        )



    return fig

'''
'''
def torta(data):
    df = data.groupby(by=['material'], ).sum()
    df.reset_index(inplace=True)
    fig = px.pie(df, values='peso', names='material', title='')
    fig.update_traces(hoverinfo="label+percent", textfont_size=14,
                      textinfo="percent", marker=dict(line=dict(color="#FFFFFF", width=0.1)),
                      textposition="auto")

    fig.update_traces(
        hovertemplate ='<b>%{label}<b><br><br><b>Peso</b>: %{value} Kg<br>')

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        legend = dict(orientation = "h",   # show entries horizontally
                     xanchor = "center",  # use center of legend as anchor
                     x = 0.5)

        )

    return fig
'''
