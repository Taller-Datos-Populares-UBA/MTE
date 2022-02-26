from dash_table import DataTable, FormatTemplate

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
    print(f"predios : {predios}")
    print(f"rutas : {rutas}")
    print(f"fecha : {fecha_inicio}")
    print(f"fecha : {fecha_finalizacion}")
    print(f"materiales : {materiales}")
    print(f"tipo_cartonero : {tipo_cartonero}")
    if predios:
        df_filtrado = df_filtrado.loc[df_filtrado['predio'].isin(predios)]
    print("1")
    if rutas:
        df_filtrado = df_filtrado.loc[df_filtrado['etapa'].isin(rutas)]
    print("2")
    df_filtrado = df_filtrado[(df_filtrado['fecha'] >= fecha_inicio) & (df_filtrado['fecha'] <= fecha_finalizacion)]
    print("3")
    if materiales:
        df_filtrado = df_filtrado.loc[df_filtrado['material'].isin(materiales)]
    print("4")
    if tipo_cartonero:
        df_filtrado = df_filtrado.loc[df_filtrado['tipoCartonero'].isin(tipo_cartonero)]
    print("5")
    return df_filtrado

def crear_tabla(id, titulos_columnas, dimensiones = ("auto", "auto"), tipos = {}, formatos = {}, es_editable = False, condicionales = []):
    """
    IMPORTANTE: Los keys de los diccionarios ``titulos_columnas``, ``tipos``, y  ``formatos`` son los id's de las columnas. Todas las columnas deben tener titulo, ya que la función consigue los id's de cada columna a traves de los keys de ``titulos_columnas``.
    """
    coulumn_ids = titulos_columnas.keys()
    columnas = []
    for col in coulumn_ids:
        nueva_columna = {
            'name': titulos_columnas[col],
            'id': col,
            'deletable': False,
            'renamable': False,
        }
        if col in tipos.keys():
            nueva_columna["type"] = tipos[col]
        if col in formatos.keys():
            nueva_columna["format"] = formatos[col]

        columnas.append(nueva_columna)


    data = {}
    for col in coulumn_ids:
        data[col] = ""

    data = [data]

    tabla = DataTable(
        id = id,
        columns = columnas,
        data = data,
        editable = es_editable,
        row_deletable = es_editable,
        style_cell = {
            "textOverflow": "ellipsis",
            "whiteSpace": "nowrap",
            "border": "1px solid black",
            "border-left": "2px solid black"
        },
        style_header = {
            "backgroundColor": "#4582ec",
            "color": "white",
            "border": "0px solid #2c559c",
        },
        style_table = {
            "height": dimensiones[1],
            "width" : dimensiones[0],
            "overflowX": "auto"
            },
        fixed_rows = {'headers': True},
        style_cell_conditional = condicionales
        )
    return tabla
