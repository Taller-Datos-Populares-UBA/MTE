# index

import dash_core_components as dcc
import dash_html_components as html
from dash import callback_context
from dash.dependencies import Output, Input, State

from app import app
from dash_index_handler import DashIndexHandler
from elements import CreateModal
from elements import NavbarElement, LogoMTE

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
    CreateModal("error5"),
    html.Div(id="page-content", children=[])
]
)

dash_handler = DashIndexHandler()


@app.callback(
    [
        Output('page-content', 'children'),
        Output("panel-navbar", "className"),
        Output("finanzas-navbar", "className"),
        Output("error5-modal", "is_open"),
        Output("header-error5", "children"),
        Output("body-error5", "children"),
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

    return dash_handler.callback(trigger, pathname, list_of_contents, list_of_names, list_of_dates)


if __name__ == "__main__":
    app.run_server(debug=False, port=9050)
