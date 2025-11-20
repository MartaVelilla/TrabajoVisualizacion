
#env\Scripts\activate
# python app.py

import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Inicializar la aplicación con soporte multi-página
app = Dash(
    __name__, 
    use_pages=True,
    external_stylesheets=[dbc.themes.COSMO],  # Opciones: BOOTSTRAP, CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN, LUX, MATERIA, MINTY, MORPH, PULSE, QUARTZ, SANDSTONE, SIMPLEX, SKETCHY, SLATE, SOLAR, SPACELAB, SUPERHERO, UNITED, VAPOR, YETI, ZEPHYR
    suppress_callback_exceptions=True,
    pages_folder="pages"
)

# Definir el servidor para despliegue
server = app.server

# Barra de navegación
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Inicio", href="/")),
        dbc.NavItem(dbc.NavLink("Sueño Diario", href="/sueno-diario")),
        dbc.NavItem(dbc.NavLink("Predictor", href="/analisis")),
        dbc.NavItem(dbc.NavLink("Información modelo", href="/visualizaciones")),
        
    ],
    brand="Proyecto Final: Sueño y Salud",
    brand_href="/",
    color="#2c3e50",
    dark=True,
    className="mb-4",
    style={"backgroundColor": "#2c3e50"}
)


# Layout principal de la aplicación
app.layout = dbc.Container([
    navbar,
    dash.page_container  # Aquí se cargan las páginas dinámicamente
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True, port=8050)

