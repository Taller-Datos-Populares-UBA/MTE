from datetime import date

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from app import app


def NavbarElement(title, asset_url, href, identifier):
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
                src=app.get_asset_url("img/logo_blanco.png"),
                className="logo-mte",
                id="logo-mte",
            ),
            href="https://mteargentina.org.ar/"
        )
    ])


def CreateButton(identificacion, txt):
    return html.Div([
        html.Button(
            children=[
                html.Img(
                    src=app.get_asset_url("img/search.svg")
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


def SelectDates(identificacion, indentificacion_radio):
    return html.Div(children=[
        html.Label("Elegí el rango de fechas", className="labels"),
        html.Div([
            dbc.RadioItems(
                options=[
                    {'label': 'Última semana', 'value': 'semana'},
                    {'label': 'Último mes', 'value': 'mes'},
                    {'label': 'Último año', 'value': 'año'},
                    {'label': 'Otro', 'value': 'otro'}
                ],
                value='otro',
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
                max_date_allowed=date(2022, 12, 31),
                start_date=date(2019, 5, 15),
                end_date=date(2021, 8, 10),
                className="date-range"
            )
        ], className="dates-container"
        )
    ])


def SelectFilterOptions(options, label, dropdown_id, response_id, capitalize=False):
    return html.Div(children=[
        html.Label(label, className="labels"),
        dcc.Dropdown(
            placeholder="Seleccionar",
            id=dropdown_id,
            className="dropdowns",
            options=[
                {"label": option.capitalize() if capitalize else option, "value": option} for option in options
            ],
            value=options,
            multi=True
        ),
        html.H6(id=response_id)]
    )


def CreateModal(idModal: str):
    return dbc.Modal(  # Modal sin informacion
        children=[
            dbc.ModalHeader(
                '',
                id=f"header-{idModal}",
                style={
                    "font-size": "30px"
                }
            ),

            dbc.ModalBody(
                '',
                id=f"body-{idModal}",
                style={
                    "font-size": "20px"
                }
            ),

            dbc.ModalFooter(
                dbc.Button(
                    children=[
                        html.Img(
                            src=app.get_asset_url("img/close.svg"),
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


def CreateFilters(predios, rutas, materiales, cartoneres):
    return html.Div(children=[

        html.H6(
            "Filtros",
            className="title-botonera"
        ),

        SelectDates("date-range", "radio-button-fechas"),
        SelectFilterOptions(predios, "Elegí el predio", "dropdown-predios", "salida-predios", capitalize=True),
        SelectFilterOptions(rutas, "Elegí la ruta o etapa", "dropdown-rutas", "salida-rutas"),
        SelectFilterOptions(materiales, "Elegí el tipo de material", "dropdown-materiales", "salida-materiales",
                            capitalize=True),
        SelectFilterOptions(cartoneres, "Elegí el tipo de cartonere", "dropdown-cartonere", "salida-cartoneres"),
    ])
