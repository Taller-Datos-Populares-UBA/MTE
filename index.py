import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from app import app
from apps import panel_control, finanzas
from elements import NavbarElement, LogoMTE

navbar = (
    html.Ul([
        NavbarElement("Panel de Control", "settings.svg", "/panel_control"),
        NavbarElement("Finanzas", "money.svg", "/finanzas"),
        NavbarElement("Bases de datos", "tune.svg", "/bases_de_datos"),
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


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/panel_control':
        return panel_control.layout
    elif pathname == '/finanzas':
        return finanzas.layout
    elif pathname == '/bases_de_datos':
        raise Exception("No implementado")
    elif pathname == "/":
        return panel_control.layout


if __name__ == "__main__":
    app.run_server(debug=True, port=9050)

# 1) Logica de tomar fecha de la computadora para devolver la ultima semana, mes, año.
# 2) Logica para conseguir tambien la fecha y automaticamente colocarla para una semana antes en el calendario de "Otro"
# 3) Logica del return del callback de ambas Tabs.
