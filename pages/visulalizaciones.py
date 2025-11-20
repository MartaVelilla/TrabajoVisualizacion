import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import ElasticNet
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from ProyectoFinal import cargar_datos
from sklearn.ensemble import RandomForestRegressor



dash.register_page(__name__, path='/visualizaciones', name='Correlaciones')


layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("Análisis de Correlaciones", className="text-center mb-2"),
                html.P("Visualización de la importancia de variables y correlaciones con la calidad del sueño",
                       className="text-center text-muted mb-4")
            ])
        ], width=12)
    ]),
    
    # Distribución de Target
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-chart-bar me-2"),
                        "Distribución de la Variable Target (Calidad del Sueño)"
                    ], className="mb-0")
                    ], className="text-white", style={"background-color": "#2c3e50"}),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div(id="stats-target-new")
                        ], width=12, lg=3, className="mb-3 mb-lg-0"),
                        dbc.Col([
                            dcc.Loading(
                                dcc.Graph(id="histogram-target-new"),
                                type="circle"
                            )
                        ], width=12, lg=9)
                    ])
                ])
            ], className="shadow mb-4")
        ], width=12)
    ]),
    
    # Importancia de Variables
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-bullseye me-2"),
                        "Importancia de Variables en el Modelo"
                    ], className="mb-0")
                ], className="text-white", style={"background-color": "#16a085"}),
                dbc.CardBody([
                    dcc.Loading(
                        dcc.Graph(id="feature-importance-new"),
                        type="circle"
                    )
                ])
            ], className="shadow mb-4")
        ], width=12)
    ]),
    
    # Heatmap de correlaciones
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4([
                        html.I(className="fas fa-th me-2"),
                        "Matriz de Correlaciones"
                    ], className="mb-0")
                ], className="text-white", style={"background-color": "#34495e"}),
                dbc.CardBody([
                    html.P("Top 20 variables más correlacionadas con la calidad del sueño",
                           className="text-muted mb-3"),
                    dcc.Loading(
                        dcc.Graph(id="heatmap-correlaciones-new"),
                        type="circle"
                    )
                ])
            ], className="shadow mb-4")
        ], width=12)
    ])
], fluid=True, className="py-4")


@callback(
    Output("stats-target-new", "children"),
    Output("histogram-target-new", "figure"),
    Output("feature-importance-new", "figure"),
    Output("heatmap-correlaciones-new", "figure"),
    Input("histogram-target-new", "id")
)
def mostrar_analisis_completo(_):
    df = cargar_datos()
    target = df['target']
    
    # ============ ESTADÍSTICAS DE TARGET ============
    stats_html = dbc.Card([
        dbc.CardBody([
            html.H5([
                html.I(className="fas fa-info-circle me-2"),
                "Estadísticas"
            ], className="text-center mb-3 text-primary"),
            
            html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P([
                            html.Strong("Mínimo:"),
                            html.Br(),
                            html.Span(f"{target.min():.1f}", className="fs-5 text-danger")
                        ], className="text-center mb-2")
                    ], width=6),
                    dbc.Col([
                        html.P([
                            html.Strong("Máximo:"),
                            html.Br(),
                            html.Span(f"{target.max():.1f}", className="fs-5 text-success")
                        ], className="text-center mb-2")
                    ], width=6),
                ]),
                
                html.Hr(className="my-2"),
                
                dbc.Row([
                    dbc.Col([
                        html.P([
                            html.Strong("Media:"),
                            html.Br(),
                            html.Span(f"{target.mean():.1f}", className="fs-5 text-info")
                        ], className="text-center mb-2")
                    ], width=6),
                    dbc.Col([
                        html.P([
                            html.Strong("Mediana:"),
                            html.Br(),
                            html.Span(f"{target.median():.1f}", className="fs-5 text-info")
                        ], className="text-center mb-2")
                    ], width=6),
                ]),
                
                html.Hr(className="my-2"),
                
                dbc.Row([
                    dbc.Col([
                        html.P([
                            html.Strong("Q1 (25%):"),
                            html.Br(),
                            html.Span(f"{target.quantile(0.25):.1f}", className="fs-6")
                        ], className="text-center mb-2")
                    ], width=6),
                    dbc.Col([
                        html.P([
                            html.Strong("Q3 (75%):"),
                            html.Br(),
                            html.Span(f"{target.quantile(0.75):.1f}", className="fs-6")
                        ], className="text-center mb-2")
                    ], width=6),
                ]),
            ])
        ])
    ], className="h-100 bg-light border-primary", style={"border-width": "2px"})
    
    # ============ HISTOGRAMA DE TARGET ============
    fig_hist = px.histogram(
        df, 
        x='target',
        nbins=40,
        title='',
        labels={'target': 'Score de Calidad del Sueño', 'count': 'Frecuencia'},
        color_discrete_sequence=["#2c3e50"]
    )
    fig_hist.update_layout(
        height=380,
        showlegend=False,
        xaxis_title="Score de Calidad del Sueño",
        yaxis_title="Frecuencia",
        plot_bgcolor='rgba(240,240,240,0.5)',
        font=dict(size=12),
        margin=dict(t=20, l=60, r=20, b=60)
    )
    fig_hist.add_vline(
        x=target.mean(), 
        line_dash="dash", 
        line_color="red", 
        annotation_text=f"Media: {target.mean():.1f}",
        annotation_position="top right"
    )
    fig_hist.add_vline(
        x=target.median(), 
        line_dash="dash", 
        line_color="green", 
        annotation_text=f"Mediana: {target.median():.1f}",
        annotation_position="top left"
    )
    
    # ============ IMPORTANCIA DE CARACTERÍSTICAS ============
    cols_sueno = [
        'Análisis del Sueño [Total] (hr)', 'Análisis del Sueño [Core] (hr)',
        'Análisis del Sueño [Deep] (hr)', 'Análisis del Sueño [REM] (hr)', 
        'Análisis del Sueño [Awake] (hr)', 'fecha'
    ]
    X = df.drop(columns=cols_sueno + ['target'], errors='ignore')
    y = df['target']
    
    # Entrenar modelo
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)
    imputer = SimpleImputer(strategy='mean')
    X_train_imputed = imputer.fit_transform(X_train)
    
    reg = RandomForestRegressor(n_estimators=100, random_state=123, max_depth=10)
    reg.fit(X_train_imputed, y_train)
    
    # Obtener coeficientes
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': reg.feature_importances_ 
    }).sort_values('Importance', ascending=True)
    
    # Top 15
    top_features = feature_importance.tail(15)
    
    # Crear colores graduales
    colors = px.colors.sequential.Viridis
    
    fig_importance = go.Figure(go.Bar(
        x=top_features['Importance'],
        y=top_features['Feature'],
        orientation='h',
        marker=dict(
            color=top_features['Importance'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Importancia", len=0.7)
        ),
        text=[f"{val:.3f}" for val in top_features['Importance']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Importancia: %{x:.4f}<extra></extra>'
    ))
    
    fig_importance.update_layout(
        title={
            'text': "Top 15 Variables Más Importantes del Modelo ElasticNet",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Importancia (Valor Absoluto del Coeficiente)",
        yaxis_title="",
        height=600,
        showlegend=False,
        font=dict(size=11),
        plot_bgcolor='rgba(240,240,240,0.5)',
        margin=dict(l=250, r=100, t=80, b=60)
    )
    
    # ============ HEATMAP DE CORRELACIONES ============
    df_num = df.select_dtypes(include='number')
    
    # Correlación con target
    correlaciones_con_target = df_num.corr()['target'].drop('target').sort_values(ascending=False)
    
    # Top 20
    top_20_vars = list(correlaciones_con_target.abs().nlargest(20).index)
    top_20_vars.append('target')
    
    corr_subset = df_num[top_20_vars].corr().round(2)
    
    fig_corr = ff.create_annotated_heatmap(
        z=corr_subset.values,
        x=list(corr_subset.columns),
        y=list(corr_subset.index),
        annotation_text=corr_subset.round(2).astype(str).values,
        colorscale='RdBu',
        showscale=True,
        reversescale=True,
        zmin=-1, 
        zmax=1,
        hovertemplate='%{y} vs %{x}<br>Correlación: %{z}<extra></extra>'
    )
    
    fig_corr.update_layout(
        title={
            'text': "Top 20 Variables Más Correlacionadas con la Calidad del Sueño",
            'x': 0.5,
            'xanchor': 'center'
        },
        height=750, 
        margin=dict(t=100, l=200, b=200, r=50), 
        font=dict(size=10),
        xaxis=dict(side='bottom', tickangle=-45),
        yaxis=dict(side='left')
    )
    
    return stats_html, fig_hist, fig_importance, fig_corr
