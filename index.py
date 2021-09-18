import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from app import app
from apps import panel_control, finanzas, error404
from elements import NavbarElement, LogoMTE

navbar = (
    html.Ul([
        NavbarElement("Panel de Control", "settings.svg", "/panel_control","panel-navbar"),
        NavbarElement("Finanzas", "money.svg", "/finanzas","finanzas-navbar"),
        #NavbarElement("Bases de datos", "tune.svg", "/bases_de_datos","bsd-navbar"), Lo dejo comentado porque supuestamente esto no va estar en la 1.0 por ahora
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


@app.callback(
    [
        Output('page-content', 'children'),
        Output("panel-navbar","className"),
        Output("finanzas-navbar","className"),
        #Output("bsd-navbar","className"),
    ],
    [
        Input('url', 'pathname')
    ]
    )
def display_page(pathname):
    if pathname == '/panel_control':
        return panel_control.layout,"link-active",""#,""
    elif pathname == '/finanzas':
        return finanzas.layout,"","link-active"#,""
    #elif pathname == '/bases_de_datos':
    #    raise Exception("No implementado")
    elif pathname == "/":
        return panel_control.layout,"link-active",""#,""
    else:
        return error404.layout,"",""


if __name__ == "__main__":
    app.run_server(debug=True, port=9050)

# 1) Logica de tomar fecha de la computadora para devolver la ultima semana, mes, año.
# 2) Logica para conseguir tambien la fecha y automaticamente colocarla para una semana antes en el calendario de "Otro"
# 3) Logica del return del callback de ambas Tabs.
