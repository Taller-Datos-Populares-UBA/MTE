import io
import base64

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from app import app
from apps import panel_control, finanzas, error404
from elements import NavbarElement, LogoMTE

from mte_dataframe import MTEDataFrame


navbar = (
    html.Ul([
        NavbarElement("Panel de Control", "settings.svg", "/panel_control", "panel-navbar"),
        NavbarElement("Finanzas", "money.svg", "/finanzas", "finanzas-navbar"),
        html.Li([
            dcc.Upload(
                id="upload-comp-base",
                multiple=True,
                children=[html.A([
                    html.Img(src=app.get_asset_url("upload.svg")),
                    "Cargar archivo"
                ])],
            )
        ]),
        html.Div(id="borrar-esto", style={"display": "hidden", "visibility": "hidden"}),
        LogoMTE(),
    ], id="navbar")
)

app.layout = html.Div([
    # Para manejar las distintas páginas/rutas
    dcc.Location(id='url', refresh=True),
    navbar,
    html.Div(id="page-content", children=[])
]
)


# BORRAR ESTO, ES PRUEBA
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    if filename.endswith(".csv"):
        file = io.StringIO(decoded.decode('utf-8'))
    elif filename.endswith(".xls") or filename.endswith(".xlsx"):
        file = io.BytesIO(decoded)

    return file


@app.callback(
    Output("borrar-esto", "children"),
    Input("upload-comp-base", "contents"),
    State("upload-comp-base", "filename"),
    State("upload-comp-base", "last_modified"),

)
def cargar_archivo(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        files_list = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        # print(files_list)
        MTEDataFrame.reset_with_files(files_list)
        df = MTEDataFrame.get_instance()
        # print(df)
        return ""


@app.callback(
    [
        Output('page-content', 'children'),
        Output("panel-navbar", "className"),
        Output("finanzas-navbar", "className"),
        # Output("bsd-navbar","className"),
    ],
    [
        Input('url', 'pathname')
    ]
    )
def display_page(pathname):
    if pathname == '/panel_control':
        return panel_control.layout, "link-active", ""  # ,""
    elif pathname == '/finanzas':
        return finanzas.layout, "", "link-active"  # ,""
    # elif pathname == '/bases_de_datos':
    #    raise Exception("No implementado")
    elif pathname == "/":
        return panel_control.layout, "link-active", ""  # ,""
    else:
        return error404.layout, "", ""


if __name__ == "__main__":
    app.run_server(debug=True, port=9050)

# 1) Logica de tomar fecha de la computadora para devolver la ultima semana, mes, año.
# 2) Logica para conseguir tambien la fecha y automaticamente colocarla para una semana antes en el calendario de "Otro"
# 3) Logica del return del callback de ambas Tabs.
