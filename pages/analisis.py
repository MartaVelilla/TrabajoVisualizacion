import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from ProyectoFinal import obtener_modelo_entrenado


dash.register_page(__name__, path='/analisis', name='Predictor de Sueño')


def get_categoria_calidad(score):
    """Obtiene la categoría de calidad basada en el score (escala 0-100)"""
    if score >= 80:
        return "Excelente", "success"
    elif score >= 70:
        return "Buena", "info"
    elif score >= 60:
        return "Aceptable", "warning"
    elif score >= 50:
        return "Regular", "warning"
    else:
        return "Mala", "danger"


def get_interpretacion(score):
    """Obtiene la interpretación basada en el score predicho"""
    categoria, _ = get_categoria_calidad(score)
    
    interpretaciones = {
        "Excelente": "Se predice que tendrás una calidad de sueño excelente. Las condiciones son óptimas para un buen descanso.",
        "Buena": "Se predice que tendrás una buena calidad de sueño. Las condiciones son favorables para descansar adecuadamente.",
        "Aceptable": "Se predice que tendrás una calidad de sueño aceptable. Hay algunas condiciones que podrían mejorar para optimizar tu descanso.",
        "Regular": "Se predice que tendrás una calidad de sueño regular. Considera mejorar las condiciones ambientales o tus hábitos antes de dormir.",
        "Mala": "Se predice que tendrás una calidad de sueño deficiente. Las condiciones actuales no son favorables. Intenta mejorar tu entorno y rutina antes de acostarte."
    }
    
    return interpretaciones.get(categoria, "No se pudo determinar la interpretación.")


# Layout de la página
layout = dbc.Container([
    html.H1("Predicción de Calidad del Sueño", className="text-center my-4"),
    html.P("Introduce tus datos del día para predecir cómo dormirás esta noche", 
           className="text-center text-muted mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("💪 Datos de Salud")),
                dbc.CardBody([
                    # Minutos de ejercicio
                    html.Label("Minutos de Ejercicio:", className="fw-bold"),
                    dcc.Slider(
                        id='input-ejercicio-pred',
                        min=0,
                        max=180,
                        step=5,
                        value=30,
                        marks={i: f'{i}min' for i in range(0, 181, 30)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    
                    # Frecuencia cardíaca media
                    html.Label("Frecuencia Cardíaca Media (bpm):", className="fw-bold mt-3"),
                    dcc.Slider(
                        id='input-fc-media-pred',
                        min=50,
                        max=120,
                        step=1,
                        value=75,
                        marks={i: str(i) for i in range(50, 121, 10)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    
                    # Frecuencia cardíaca mínima
                    html.Label("Frecuencia Cardíaca Mínima (bpm):", className="fw-bold mt-3"),
                    dcc.Slider(
                        id='input-fc-min-pred',
                        min=40,
                        max=80,
                        step=1,
                        value=55,
                        marks={i: str(i) for i in range(40, 81, 10)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    
                    # Frecuencia cardíaca máxima
                    html.Label("Frecuencia Cardíaca Máxima (bpm):", className="fw-bold mt-3"),
                    dcc.Slider(
                        id='input-fc-max-pred',
                        min=80,
                        max=200,
                        step=1,
                        value=140,
                        marks={i: str(i) for i in range(80, 201, 20)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    
                    # HRV
                    html.Label("Variabilidad Frecuencia Cardíaca - HRV (ms):", className="fw-bold mt-3"),
                    dcc.Slider(
                        id='input-hrv-pred',
                        min=0,
                        max=200,
                        step=5,
                        value=50,
                        marks={i: f'{i}' for i in range(0, 201, 40)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                ])
            ], className="shadow mb-3")
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("🌤️ Condiciones Ambientales")),
                dbc.CardBody([
                    # Temperatura ambiente
                    html.Label("Temperatura Ambiente (°C):", className="fw-bold"),
                    dcc.Slider(
                        id='input-temperatura-pred',
                        min=-5,
                        max=35,
                        step=0.5,
                        value=20,
                        marks={i: f'{i}°' for i in range(-5, 36, 5)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    
                    # Humedad
                    html.Label("Humedad Relativa (%):", className="fw-bold mt-3"),
                    dcc.Slider(
                        id='input-humedad-pred',
                        min=0,
                        max=100,
                        step=5,
                        value=50,
                        marks={i: f'{i}%' for i in range(0, 101, 20)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    
                    # Presión atmosférica
                    html.Label("Presión Atmosférica (hPa):", className="fw-bold mt-3"),
                    dcc.Slider(
                        id='input-presion-pred',
                        min=980,
                        max=1040,
                        step=1,
                        value=1013,
                        marks={i: str(i) for i in range(980, 1041, 10)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    
                    # Precipitación
                    html.Label("Precipitación (mm):", className="fw-bold mt-3"),
                    dcc.Slider(
                        id='input-precipitacion-pred',
                        min=0,
                        max=10,
                        step=0.5,
                        value=0,
                        marks={i: f'{i}' for i in range(0, 11, 2)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    
                    # Viento
                    html.Label("Velocidad del Viento (km/h):", className="fw-bold mt-3"),
                    dcc.Slider(
                        id='input-viento-pred',
                        min=0,
                        max=60,
                        step=1,
                        value=15,
                        marks={i: str(i) for i in range(0, 61, 10)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                ])
            ], className="shadow mb-3")
        ], md=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Button(
                "Predecir Calidad del Sueño",
                id="btn-predecir-pred",
                className="w-100 mt-3 mb-4",
                size="lg",
                style={"backgroundColor": "#2c3e50", "borderColor": "#2c3e50"}
            )
        ], md=12)
    ]),
    
    # SOLO UN DIV VACÍO - La card aparecerá después de predecir
    html.Div(id='resultado-prediccion-pred', className="mt-4")
], fluid=True)


# Callback para la predicción
@dash.callback(
    Output('resultado-prediccion-pred', 'children'),
    Input('btn-predecir-pred', 'n_clicks'),
    State('input-ejercicio-pred', 'value'),
    State('input-fc-media-pred', 'value'),
    State('input-fc-min-pred', 'value'),
    State('input-fc-max-pred', 'value'),
    State('input-hrv-pred', 'value'),
    State('input-temperatura-pred', 'value'),
    State('input-humedad-pred', 'value'),
    State('input-presion-pred', 'value'),
    State('input-precipitacion-pred', 'value'),
    State('input-viento-pred', 'value'),
    prevent_initial_call=True
)
def predecir_calidad(n_clicks, ejercicio, fc_media, fc_min, fc_max, hrv, 
                     temperatura, humedad, presion, precipitacion, viento):
    if n_clicks is None:
        return html.Div()  # Devuelve vacío si no se ha hecho clic
    
    try:
        # Obtener modelo entrenado e imputer
        modelo, imputer, X_train = obtener_modelo_entrenado()
        
        # Inicializar con medias del entrenamiento
        user_data = pd.DataFrame(0, index=[0], columns=X_train.columns)
        for col in X_train.columns:
            user_data[col] = X_train[col].mean()
        
        # DATOS DE SALUD
        if 'Minutos de Ejercicio (min)' in user_data.columns:
            user_data['Minutos de Ejercicio (min)'] = ejercicio
        if 'Frecuencia Cardíaca (count/min)' in user_data.columns:
            user_data['Frecuencia Cardíaca (count/min)'] = fc_media
        if 'Frecuencia Cardíaca Mínima (count/min)' in user_data.columns:
            user_data['Frecuencia Cardíaca Mínima (count/min)'] = fc_min
        if 'Frecuencia Cardíaca Máxima (count/min)' in user_data.columns:
            user_data['Frecuencia Cardíaca Máxima (count/min)'] = fc_max
        if 'Variabilidad de Frecuencia Cardíaca (ms) ' in user_data.columns:
            user_data['Variabilidad de Frecuencia Cardíaca (ms) '] = hrv
        
        # DATOS METEOROLÓGICOS
        if 'Temperature' in user_data.columns:
            user_data['Temperature'] = temperatura
        if 'Humidity (%)' in user_data.columns:
            user_data['Humidity (%)'] = humedad
        if 'Mean Sea Level Pressure (hPa)' in user_data.columns:
            user_data['Mean Sea Level Pressure (hPa)'] = presion
        if 'Precipitation Total' in user_data.columns:
            user_data['Precipitation Total'] = precipitacion
        if 'Wind Gust' in user_data.columns:
            user_data['Wind Gust'] = viento
        
        # Aplicar el imputer
        user_data_imputed = imputer.transform(user_data)
        
        # Realizar la predicción
        prediccion = modelo.predict(user_data_imputed)[0]
        
        # Asegurar que la predicción esté en el rango 0-100
        prediccion = np.clip(prediccion, 0, 100)
        
        # Obtener categoría y color
        categoria, color = get_categoria_calidad(prediccion)
        
        # Obtener interpretación
        interpretacion = get_interpretacion(prediccion)
        
        # AHORA SÍ CREAR LA CARD CON EL RESULTADO
        resultado = dbc.Card([
            dbc.CardHeader(html.H4("Predicción"), className="text-center"),
            dbc.CardBody([
                html.H2(f"Puntuación Predicha: {prediccion:.1f}/100", className="mb-3 text-center"),
                dbc.Progress(
                    value=prediccion,
                    max=100,
                    color=color,
                    className="mb-3",
                    style={"height": "30px"}
                ),
                dbc.Alert([
                    html.H4(f"Calidad Predicha: {categoria}", className="alert-heading"),
                    html.Hr(),
                    html.P(interpretacion, className="mb-0")
                ], color=color),
                
                # Detalles en dos columnas
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("💪 Datos de Salud"),
                            dbc.CardBody([
                                html.Ul([
                                    html.Li(f"Ejercicio: {ejercicio} min"),
                                    html.Li(f"FC Media: {fc_media} bpm"),
                                    html.Li(f"FC Mín: {fc_min} bpm"),
                                    html.Li(f"FC Máx: {fc_max} bpm"),
                                    html.Li(f"HRV: {hrv} ms")
                                ])
                            ])
                        ], className="mt-3")
                    ], md=6),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("🌤️ Condiciones Ambientales"),
                            dbc.CardBody([
                                html.Ul([
                                    html.Li(f"Temperatura: {temperatura}°C"),
                                    html.Li(f"Humedad: {humedad}%"),
                                    html.Li(f"Presión: {presion} hPa"),
                                    html.Li(f"Precipitación: {precipitacion} mm"),
                                    html.Li(f"Viento: {viento} km/h")
                                ])
                            ])
                        ], className="mt-3")
                    ], md=6)
                ])
            ])
        ], className="shadow")
        
        return resultado
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return dbc.Card([
            dbc.CardHeader(html.H4("Error"), className="text-center"),
            dbc.CardBody([
                dbc.Alert([
                    html.H5("Error al realizar la predicción"),
                    html.Hr(),
                    html.P(f"Mensaje: {str(e)}"),
                    html.Pre(error_detail, style={"fontSize": "10px", "maxHeight": "300px", "overflow": "auto"})
                ], color="danger")
            ])
        ], className="shadow")
