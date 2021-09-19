import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from datetime import date, datetime, timedelta

from app import app


def NavbarElement(title, asset_url, href,identifier):
    return html.Li([
        html.A([
            html.Img(
                src=app.get_asset_url(asset_url)
            ),
            html.P(title)
        ],
            href=href
        )
    ],        
    id=identifier,
    )

def LogoMTE():
    return html.Li([
        html.A(
            html.Img(
                src=app.get_asset_url("logo_blanco.png"),
                className="logo-mte",
                id="logo-mte",
            ),
            href="https://mteargentina.org.ar/"
        )
    ])

def CreateButton(identificacion,txt):
    return html.Div([
        html.Button(
            children=[
                html.Img(
                    src=app.get_asset_url("search.svg")
                ),

                html.P(
                    txt
                )
                ],
            id=identificacion,
            n_clicks=0,
            className="mr-1 mt-1 btn btn-primary search-button"

        ),
    ],
    className="button-container")

def SelectDates(identificacion,indentificacion_radio):
    return html.Div(children=[
            html.Label("Elegí el rango de fechas",className="labels"),
            html.Div([
                dbc.RadioItems(
                        options=[
                                {'label': 'Última semana', 'value': 'semana'},
                                {'label': 'Último mes', 'value': 'mes'},
                                {'label': 'Último año', 'value': 'año'},
                                {'label': 'Otro', 'value': 'otro'}
                        ],
                        value='semana',
                        className="radio-item",
                        style={
                                "fontSize": "18px",
                                "width": "100%",
                        },
                        id=indentificacion_radio
                ),    
                dcc.DatePickerRange(
                    id=identificacion,
                    display_format="D/M/Y",
                    min_date_allowed=date(1995, 8, 5),
                    max_date_allowed=date(2021, 12, 31),
                    start_date=date(2019, 5, 15),
                    end_date=date(2021, 8, 10),
                    className="date-range"
                )
                ],className="dates-container"
                )
    ])

def SelectFilterOptions(options, label, dropdown_id, response_id, add_all_as_option=False, capitalize=False):
    options = list(options) + ["Todas"] if add_all_as_option else options
    initial_value = "Todas" if add_all_as_option else options
    return html.Div(children=[
        html.Label(label,className="labels"),
        dcc.Dropdown(
            placeholder="Seleccionar",
            id=dropdown_id,
            className="dropdowns",
            options=[
                {"label": option.capitalize() if capitalize else option, "value": option} for option in options
            ],
            value=initial_value,
            multi=True
        ),
        html.H6(id=response_id)]
    )

def CreateModal(idModal:str,titleModal:str,bodyModal:str):
    return dbc.Modal(  # Modal sin informacion
        children=[
            dbc.ModalHeader(
                titleModal,
                style={
                    "font-size": "30px"
                }
            ),

            dbc.ModalBody(
                bodyModal,
                style={
                    "font-size": "20px"
                }
            ),

            dbc.ModalFooter(
                dbc.Button(
                    children=[
                        html.Img(
                            src=app.get_asset_url("close.svg"),
                            className="ico"),
                        "Cerrar"
                    ],
                    id=f"close-modal-{idModal}-button",
                    className="mr-1 mt-1 btn btn-primary modal-button",
                    n_clicks=0,
                )
            ),
        ],
        id=f"{idModal}-modal",
        is_open=False,
        backdrop="static"  # Modal sin informacion
    )
