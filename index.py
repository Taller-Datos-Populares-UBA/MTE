# index

import base64
import io

import dash_core_components as dcc
import dash_html_components as html
from dash import callback_context
from dash.dependencies import Output, Input, State

from app import app
from apps import panel_control, finanzas, error404
from elements import NavbarElement, LogoMTE
from mte_dataframe import MTEDataFrame

navbar = (
    html.Ul([
        NavbarElement("Panel de Control", "img/settings.svg", "/panel_control", "panel-navbar"),
        NavbarElement("Finanzas", "img/money.svg", "/finanzas", "finanzas-navbar"),
        html.Li([
            dcc.Upload(
                id="upload-comp-base",
                multiple=True,
                children=[html.A([
                    html.Img(src=app.get_asset_url("img/upload.svg")),
                    "Cargar archivo"
                ])],
            )
        ]),
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


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    if filename.endswith(".csv"):
        return io.StringIO(decoded.decode('utf-8'))
    elif filename.endswith(".xls") or filename.endswith(".xlsx"):
        return io.BytesIO(decoded)

    return None  # TODO It should raise an exception


@app.callback(
    [
        Output('page-content', 'children'),
        Output("panel-navbar", "className"),
        Output("finanzas-navbar", "className"),
    ],
    [
        Input('url', 'pathname'),
        Input('upload-comp-base', 'contents'),
        State('upload-comp-base', 'filename'),
        State('upload-comp-base', 'last_modified'),
    ]
)
def display_page(pathname, list_of_contents, list_of_names, list_of_dates):
    trigger = callback_context.triggered[0]

    if trigger["prop_id"] == "upload-comp-base.contents":
        if list_of_contents is not None:
            files_list = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            MTEDataFrame.reset_with_files(files_list)

    if MTEDataFrame.FILES_TO_LOAD:
        predios, rutas, materiales, cartoneres = MTEDataFrame.create_features()
    else:
        predios, rutas, materiales, cartoneres = [], [], [], []

    if pathname == '/panel_control':
        return panel_control.layout(predios, rutas, materiales, cartoneres), "link-active", ""  # ,""
    elif pathname == '/finanzas':
        return finanzas.layout(predios, rutas, materiales, cartoneres), "", "link-active"  # ,""
    elif pathname == '/':
        return panel_control.layout(predios, rutas, materiales, cartoneres), "link-active", ""  # ,""
    else:
        return error404.layout, "", ""


if __name__ == "__main__":
    app.run_server(debug=True, port=9050)
