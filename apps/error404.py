import dash_html_components as html

layout = html.Div([
	html.Div(
		id="parent-error",
		className="parent-error",
		children=[
			html.Div(
				children=[
					html.Div(children=["Oops!"],className="error-404"),
					html.Div(children=[html.Div("Página no encontrada.",id="page-not-found"),html.Div("Prueba a volver con la barra de navegación.",id="hint-error")], className="page-not-found")
				],
				className="wrapper-error")
		],
		)
])