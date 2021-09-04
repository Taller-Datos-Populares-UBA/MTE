import dash_html_components as html

from app import app


def NavbarElement(title, asset_url, href):
    return html.Li([
        html.A([
            html.Img(
                src=app.get_asset_url(asset_url)
            ),
            html.P(title)
        ],
            href=href
        )
    ])


def LogoMTE():
    return html.Li([
        html.A(
            html.Img(
                src=app.get_asset_url("logo_blanco.png"),
                className="logo-mte-finanzas",
                id="logo-mte-finanzas",
            ),
            href="https://mteargentina.org.ar/"
        )
    ])
