
def determinar_tipo_cartonero(row):
    if row['legacyId'].startswith('LE'):
        val = 'LE'
    elif row['legacyId'] == 'No especificado':
        val = 'No especificado'
    else:
        val = 'RA'
    return val


def crear_df_filtrado(df, predios, rutas, fecha_inicio, fecha_finalizacion, materiales, tipo_cartonero):
    """
    Si el dropdown queda vacío, nos llega una lista vacía y eso implica que devolvemos
    un df sin filtrar en esa categoría (por eso los condicionales).
    """
    df_filtrado = df.copy()

    # crear columna de tipos de cartoneres, esto hay que moverlo al singleton
    # df_filtrado['tipoCartonero'] = df_filtrado.apply(determinar_tipo_cartonero, axis=1)

    # aplicar filtros
    if predios:
        df_filtrado = df_filtrado.loc[df_filtrado['predio'].isin(predios)]

    if rutas:
        df_filtrado = df_filtrado.loc[df_filtrado['etapa'].isin(rutas)]

    df_filtrado = df_filtrado[(df_filtrado['fecha'] >= fecha_inicio) & (df_filtrado['fecha'] <= fecha_finalizacion)]

    if materiales:
        df_filtrado = df_filtrado.loc[df_filtrado['material'].isin(materiales)]

    if tipo_cartonero:
        df_filtrado = df_filtrado.loc[df_filtrado['tipoCartonero'].isin(tipo_cartonero)]

    return df_filtrado
