import plotly.express as px


# Funcion para crear columna de tipo de cartonere
def determinar_tipo_cartonero(row):
    if row['legacyId'].startswith('LE'):
        val = 'LE'
    elif row['legacyId'] == 'No especificado':
        val = 'No especificado'
    else:
        val = 'RA'
    return val


def crear_df_filtrado(df, predios, fecha_inicio, fecha_finalizacion, materiales, tipo_cartonero):
    df_filtrado = df.copy()

    # Crear columna de tipos de cartoneres
    df_filtrado['tipoCartonero'] = df_filtrado.apply(determinar_tipo_cartonero, axis=1)

    # Aplicar filtros
    df_filtrado = df_filtrado.loc[df_filtrado['predio'].isin(predios)]
    df_filtrado = df_filtrado[(df_filtrado['fecha'] >= fecha_inicio) & (df_filtrado['fecha'] <= fecha_finalizacion)]
    df_filtrado = df_filtrado.loc[df_filtrado['material'].isin(materiales)]
    df_filtrado = df_filtrado.loc[df_filtrado['tipoCartonero'].isin(tipo_cartonero)]

    return df_filtrado


def pesos_historico(data, operacion='promedio'):
    if operacion == 'promedio':
        df = data.groupby(by=['fecha', 'predio'], ).mean()
    else:
        df = data.groupby(by=['fecha', 'predio'], ).sum()
    df.reset_index(inplace=True)
    fig = px.scatter(df, x="fecha", y="peso", color="predio", size="peso")
    return fig


def torta(data):
    df = data.groupby(by=['material'], ).sum()
    df.reset_index(inplace=True)
    fig = px.pie(df, values='peso', names='material', title='')
    fig.update_traces(hoverinfo="label+percent", textfont_size=14,
                      textinfo="percent", marker=dict(line=dict(color="#FFFFFF", width=0.1)),
                      textposition="auto")
    return fig
