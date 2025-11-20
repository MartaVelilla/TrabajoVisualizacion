import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from ProyectoFinal import cargar_datos


dash.register_page(__name__, path='/sueno-diario', name='Sueño Diario')


def get_categoria_por_horas(horas_totales):
    """
    Categoriza la calidad del sueño según las HORAS TOTALES
    """
    if horas_totales >= 8:
        return "Excelente", "success"
    elif horas_totales >= 7:
        return "Buena", "info"
    elif horas_totales >= 6:
        return "Aceptable", "warning"
    elif horas_totales >= 5:
        return "Regular", "warning"
    else:
        return "Mala", "danger"


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.I(className="fas fa-moon fa-2x me-3", style={"color": "#6366f1"}),
                html.H2("Análisis Diario del Sueño", className="d-inline-block mb-0"),
            ], className="d-flex align-items-center justify-content-center mb-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("📅 Selecciona una fecha:", className="fw-bold mb-2", style={"fontSize": "1.1rem"}),
                    dcc.Dropdown(
                        id='dropdown-fecha',
                        placeholder='Selecciona una fecha...',
                        className="mb-3",
                        style={"fontSize": "1rem"}
                    )
                ])
            ], className="shadow-sm")
        ], width=12, lg=6, className="mx-auto")
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='cards-info', className="mb-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='pie-chart-sueno', config={'displayModeBar': False})
                ])
            ], className="shadow")
        ], width=12, lg=8, className="mx-auto")
    ])
], fluid=True, style={"backgroundColor": "#f8f9fa", "minHeight": "100vh", "padding": "2rem"})


@callback(
    Output('dropdown-fecha', 'options'),
    Output('dropdown-fecha', 'value'),
    Input('dropdown-fecha', 'id')
)
def cargar_fechas(_):
    try:
        df = cargar_datos()
        fechas = sorted(list(df['fecha'].unique()), reverse=True)
        options = [{'label': str(f), 'value': str(f)} for f in fechas]
        valor_inicial = str(fechas[0]) if fechas else None
        return options, valor_inicial
    except Exception as e:
        return [], None


@callback(
    Output('pie-chart-sueno', 'figure'),
    Output('cards-info', 'children'),
    Input('dropdown-fecha', 'value')
)
def actualizar_dashboard(fecha_seleccionada):
    import datetime
    df = cargar_datos()
    
    if not fecha_seleccionada:
        return go.Figure(), dbc.Alert("Selecciona una fecha para ver los datos.", color="info", className="text-center")
    
    if isinstance(fecha_seleccionada, str):
        fecha_sel = datetime.datetime.strptime(fecha_seleccionada, '%Y-%m-%d').date()
    else:
        fecha_sel = fecha_seleccionada
    
    df_sel = df[df['fecha'] == fecha_sel]
    
    if df_sel.empty:
        return go.Figure(), dbc.Alert(f"No hay datos para {fecha_seleccionada}.", color="warning", className="text-center")
    
    # ====== USAR HORAS TOTALES EN VEZ DE TARGET ======
    horas_totales = df_sel.iloc[0]['Análisis del Sueño [Total] (hr)']
    calidad, color_badge = get_categoria_por_horas(horas_totales)
    
    # Datos del gráfico (sin incluir "Total" ni "Awake")
    columnas = [
        "Análisis del Sueño [Core] (hr)",
        "Análisis del Sueño [Deep] (hr)",
        "Análisis del Sueño [REM] (hr)",
        "Análisis del Sueño [Awake] (hr)",
    ]
    etiquetas = ["Core", "Profundo", "REM", "Despierto"]
    valores = df_sel.iloc[0][columnas].values.astype(float)
    
    # Datos meteorológicos
    temperatura = df_sel.iloc[0].get('Temperature', 'N/A')
    precipitacion = df_sel.iloc[0].get('Precipitation Total', 'N/A')
    
    # Cards informativos
    cards = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Calidad de sueño (%)", className="text-muted mb-2"),
                    html.H2(f"{horas_totales:.1f}h", className="mb-0 fw-bold"),  # MOSTRAR HORAS
                    dbc.Badge(calidad, color=color_badge, className="mt-2", pill=True)
                ], className="text-center")
            ], className="shadow-sm h-100")
        ], width=12, md=4, className="mb-3"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Temperatura media (°C)", className="text-muted mb-2"),
                    html.H3(f"{temperatura:.1f}°C" if temperatura != 'N/A' else "N/A", className="mb-0")
                ], className="text-center")
            ], className="shadow-sm h-100", color="light")
        ], width=12, md=4, className="mb-3"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Precipitación (mm)", className="text-muted mb-2"),
                    html.H3(f"{precipitacion:.1f} mm" if precipitacion != 'N/A' else "N/A", className="mb-0")
                ], className="text-center")
            ], className="shadow-sm h-100", color="light")
        ], width=12, md=4, className="mb-3"),
    ])
    
    # Gráfico de pastel mejorado
    colors = ['#3b82f6', '#8b5cf6', '#10b981', '#ef4444']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=etiquetas,
            values=valores,
            hole=0.4,
            marker=dict(
                colors=colors,
                line=dict(color='white', width=3)
            ),
            textposition='outside',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Horas: %{value:.2f}<br>Porcentaje: %{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=f"Distribución del Sueño - {fecha_sel}",
            font=dict(size=20, color="#1f2937"),
            x=0.5,
            xanchor='center'
        ),
        annotations=[dict(
            text=f'{horas_totales:.1f}h<br>totales',  # MOSTRAR HORAS TOTALES
            x=0.5, y=0.5,
            font=dict(size=20, color="#6b7280"),
            showarrow=False
        )],
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14)
    )
    
    return fig, cards
