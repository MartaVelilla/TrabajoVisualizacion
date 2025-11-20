import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Registrar la página como la página principal
dash.register_page(__name__, path='/', name='Inicio')

# Definir el layout de la página de inicio
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Proyecto Final: Sueño y Salud", className="text-center mb-4"),
            html.Hr(),
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3("Bienvenido al portal de análisis del sueño", className="card-title"),
                    html.P(
                        """Dormir bien es uno de los pilares fundamentales para mantener una buena 
                        salud física, mental y emocional. El sueño no solo permite que el cuerpo 
                        descanse y recupere energía, sino que también tiene un papel clave en la 
                        consolidación de la memoria, en la reparación de tejidos, en el equilibrio 
                        hormonal y en la regulación del sistema inmunológico. Diversos estudios 
                        científicos han demostrado que una buena calidad y cantidad de sueño 
                        contribuyen a mejorar el rendimiento cognitivo, el estado de ánimo, la 
                        creatividad y la capacidad de tomar decisiones.""",
                        className="card-text"
                    ),
                ])
            ], className="mb-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Efectos de la Privación del Sueño", className="card-title"),
                    html.P(
                        """Por el contrario, dormir mal o de forma insuficiente puede tener efectos 
                        negativos inmediatos y acumulativos. La privación de sueño se asocia con un 
                        mayor riesgo de desarrollar enfermedades como hipertensión, obesidad, diabetes, 
                        depresión e incluso problemas cardiovasculares. Además, la falta de sueño 
                        afecta la concentración, la coordinación motora y la capacidad de reacción, 
                        aumentando la probabilidad de sufrir accidentes o cometer errores.""",
                        className="card-text"
                    ),
                ])
            ], className="mb-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Importancia del Descanso en el Mundo Moderno", className="card-title"),
                    html.P(
                        """En un mundo cada vez más acelerado y digitalizado, donde el estrés y los 
                        estímulos están presentes a lo largo del día, aprender a valorar y proteger 
                        el descanso nocturno es más importante que nunca. Mejorar los hábitos de 
                        sueño no solo favorece nuestro bienestar diario, sino que es un factor 
                        determinante para alcanzar una vida más sana, equilibrada y productiva.""",
                        className="card-text"
                    ),
                ])
            ], className="mb-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Alert([
                html.I(className="fas fa-info-circle me-2"),
                "Selecciona una página del menú superior para ver los resultados del análisis."
            ], color="info")
        ], width=12)
    ])
], fluid=True)
