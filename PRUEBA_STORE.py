import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable, FormatTemplate
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

app = dash.Dash()

app.layout = html.Div([
    html.H1("Probando store"),
    dcc.Store(
        id="store-precios",
        storage_type="local"
    ),
    html.Div(
        id="div-tabla",
        children=[
            DataTable(
                id='tabla',
                columns=[
                    {
                        'name': 'Sede',
                        'id': 'sede',
                        'deletable': False,
                        'renamable': False,
                    },
                    {
                        'name': 'Material',
                        'id': 'material',
                        'deletable': False,
                        'renamable': False,
                    },
                    {
                        'name': '  Precio RA',
                        'id': 'preciora',
                        'deletable': False,
                        'renamable': False,
                        "type": 'numeric',
                        "format": FormatTemplate.money(2)
                    },
                    {
                        'name': '  Precio LE',
                        'id': 'preciole',
                        'deletable': False,
                        'renamable': False,
                        "type": 'numeric',
                        "format": FormatTemplate.money(2)
                    }
                ],
                data=[
                    {"material": "", "preciora": "",
                        "preciole": "",
                        "sede": ""}
                ],
                editable=True,
                row_deletable=True,
                style_cell={
                    "textOverflow": "ellipsis",
                    "whiteSpace": "nowrap",
                    "border": "1px solid black",
                    "border-left": "2px solid black"
                },
                style_header={
                    "backgroundColor": "#4582ec",
                    "color": "white",
                    "border": "0px solid #2c559c",
                },
                style_table={
                    "height": "200px",
                    "minHeight": "200px",
                    "maxHeight": "200px",
                    "overflowX": "auto"
                },
                fixed_rows={'headers': True},
                style_cell_conditional=[
                    {'if': {'column_id': 'sede'},
                        'width': '150px'},
                    {'if': {'column_id': 'material'},
                        'width': '150px'},
                    {'if': {'column_id': 'preciora'},
                        'width': '100px'},
                    {'if': {'column_id': 'preciole'},
                        'width': '100px'},
                    {'if': {'column_id': ''},
                        'width': '25em'},
                ]

            ),
        ]
    ),
    html.Button(
        id="agregar-fila",
        children=["Agregar fila"]
    ),
])


@app.callback(
    Output("tabla", "data"),
    Output("store-precios", "data"),
    Input("agregar-fila", "n_clicks"),
    Input("tabla", "selected_cells"),
    State("tabla", "data"),
    State("tabla", "columns"),
    State("store-precios", "data")
)
def agregar_fila(click_add, selected_cells, rows, columns, store_data):
    if store_data:
        print("STORE:", store_data)
    if selected_cells:
        return rows, rows
    if click_add:
        if rows == None:
            if store_data:
                rows = store_data
                rows.append(({c['id']: '' for c in columns}))
            else:
                rows = [{c['id']: '' for c in columns}]
        else:
            rows.append(({c['id']: '' for c in columns}))
        print((rows, rows))
        return (rows, rows)
    else:
        if store_data:
            rows = store_data
        else:
            rows = None
        return rows, rows


if __name__ == "__main__":
    app.run_server(debug=True)
