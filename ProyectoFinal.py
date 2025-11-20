import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error


def cargar_datos():
    """Carga y procesa los datos para el modelo"""
    df = pd.read_csv("HealthDataSet.csv", sep=",", encoding="utf-8-sig", index_col=False)
    df2 = pd.read_csv("datos_diarios_limpios.csv", sep=",")
    
    df = df.dropna(how='all', axis=1)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df2['fecha'] = pd.to_datetime(df2['fecha']).dt.date
    df = df.rename(columns={'Date': 'fecha'})
    df_merged = pd.merge(df, df2, on='fecha', how='inner')

    # ====== NUEVO CÁLCULO DE TARGET ======
    # 1. Componente de DURACIÓN (50% del score)
    # Normalizar horas totales: 8h = 100%, 0h = 0%
    horas_ideal = 8.0
    df_merged["score_duracion"] = np.clip(
        (df_merged["Análisis del Sueño [Total] (hr)"] / horas_ideal) * 50, 
        0, 50
    )
    
    # 2. Componente de CALIDAD (30% del score)
    # Proporciones de sueño profundo y REM
    df_merged["deep_ratio"] = df_merged["Análisis del Sueño [Deep] (hr)"] / df_merged["Análisis del Sueño [Total] (hr)"]
    df_merged["rem_ratio"] = df_merged["Análisis del Sueño [REM] (hr)"] / df_merged["Análisis del Sueño [Total] (hr)"]
    
    # Ideales: Deep ~15-20%, REM ~20-25%
    df_merged["score_deep"] = np.clip((df_merged["deep_ratio"] / 0.20) * 15, 0, 15)
    df_merged["score_rem"] = np.clip((df_merged["rem_ratio"] / 0.25) * 15, 0, 15)
    df_merged["score_calidad"] = df_merged["score_deep"] + df_merged["score_rem"]
    
    # 3. Componente de RECUPERACIÓN (20% del score)
    # HRV normalizada
    df_merged["hrv_norm"] = (
        (df_merged["Variabilidad de Frecuencia Cardíaca (ms) "] - df_merged["Variabilidad de Frecuencia Cardíaca (ms) "].min()) /
        (df_merged["Variabilidad de Frecuencia Cardíaca (ms) "].max() - df_merged["Variabilidad de Frecuencia Cardíaca (ms) "].min())
    )
    df_merged["score_recuperacion"] = df_merged["hrv_norm"] * 20
    
    # 4. TARGET FINAL (escala 0-100)
    df_merged["target"] = (
        df_merged["score_duracion"] +      # 50 puntos
        df_merged["score_calidad"] +       # 30 puntos
        df_merged["score_recuperacion"]    # 20 puntos
    )
    
    # Eliminar columnas temporales
    cols_to_drop = [
        "Análisis del Sueño [Asleep] (hr)", "Análisis del Sueño [In Bed] (hr)",
        "Minutos Conscientes (min)", "Growing Degree Days",
        "Promedio de Frecuencia Cardíaca al Caminar (count/min)",
        "Tiempo en Luz de Día (min)", 
        "deep_ratio", "rem_ratio", "hrv_norm", 
        "score_duracion", "score_deep", "score_rem", "score_calidad", "score_recuperacion"
    ]
    df_merged = df_merged.drop(columns=cols_to_drop, errors='ignore')

    # Filtrar filas con valores nulos en columnas clave
    sleep_cols = [
        "Análisis del Sueño [Total] (hr)", "Análisis del Sueño [Core] (hr)",
        "Análisis del Sueño [Deep] (hr)", "Análisis del Sueño [REM] (hr)",
        "Análisis del Sueño [Awake] (hr)", "target"
    ]
    df_merged = df_merged.dropna(subset=sleep_cols)
    return df_merged


def entrenar_modelo(df_merged):
    """Entrena el modelo y devuelve métricas"""
    cols_sueno = [
        'Análisis del Sueño [Total] (hr)', 'Análisis del Sueño [Core] (hr)',
        'Análisis del Sueño [Deep] (hr)', 'Análisis del Sueño [REM] (hr)', 
        'Análisis del Sueño [Awake] (hr)', 'fecha'
    ]
    X = df_merged.drop(columns=cols_sueno + ['target'], errors='ignore')
    y = df_merged['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)
    imputer = SimpleImputer(strategy='mean')
    X_train_imputed = imputer.fit_transform(X_train)
    X_test_imputed = imputer.transform(X_test)
    mask_train = ~y_train.isna()
    X_train_imputed, y_train = X_train_imputed[mask_train], y_train[mask_train]
    mask_test = ~y_test.isna()
    X_test_imputed, y_test = X_test_imputed[mask_test], y_test[mask_test]

    reg = ElasticNet()
    reg.fit(X_train_imputed, y_train)
    pred_train = reg.predict(X_train_imputed)
    pred_test = reg.predict(X_test_imputed)

    rmse_train = np.sqrt(mean_squared_error(y_train, pred_train))
    mae_train = mean_absolute_error(y_train, pred_train)
    mape_train = mean_absolute_percentage_error(y_train, pred_train)
    rmse_test = np.sqrt(mean_squared_error(y_test, pred_test))
    mae_test = mean_absolute_error(y_test, pred_test)
    mape_test = mean_absolute_percentage_error(y_test, pred_test)
    
    metrics = {
        "RMSE train": round(rmse_train, 3),
        "MAE train": round(mae_train, 3),
        "MAPE train": f"{100 * mape_train:.2f}%",
        "RMSE test": round(rmse_test, 3),
        "MAE test": round(mae_test, 3),
        "MAPE test": f"{100 * mape_test:.2f}%"
    }
    return metrics


def cargar_datos_todos():
    """Carga todos los datos sin filtrar para visualizaciones"""
    df = pd.read_csv("HealthDataSet.csv", sep=",", encoding="utf-8-sig", index_col=False)
    df2 = pd.read_csv("datos_diarios_limpios.csv", sep=",")
    
    df = df.dropna(how='all', axis=1)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df2['fecha'] = pd.to_datetime(df2['fecha']).dt.date
    df = df.rename(columns={'Date': 'fecha'})
    df_merged = pd.merge(df, df2, on='fecha', how='inner')

    # MISMO CÁLCULO QUE EN cargar_datos()
    horas_ideal = 8.0
    df_merged["score_duracion"] = np.clip(
        (df_merged["Análisis del Sueño [Total] (hr)"] / horas_ideal) * 50, 
        0, 50
    )
    
    df_merged["deep_ratio"] = df_merged["Análisis del Sueño [Deep] (hr)"] / df_merged["Análisis del Sueño [Total] (hr)"]
    df_merged["rem_ratio"] = df_merged["Análisis del Sueño [REM] (hr)"] / df_merged["Análisis del Sueño [Total] (hr)"]
    
    df_merged["score_deep"] = np.clip((df_merged["deep_ratio"] / 0.20) * 15, 0, 15)
    df_merged["score_rem"] = np.clip((df_merged["rem_ratio"] / 0.25) * 15, 0, 15)
    df_merged["score_calidad"] = df_merged["score_deep"] + df_merged["score_rem"]
    
    df_merged["hrv_norm"] = (
        (df_merged["Variabilidad de Frecuencia Cardíaca (ms) "] - df_merged["Variabilidad de Frecuencia Cardíaca (ms) "].min()) /
        (df_merged["Variabilidad de Frecuencia Cardíaca (ms) "].max() - df_merged["Variabilidad de Frecuencia Cardíaca (ms) "].min())
    )
    df_merged["score_recuperacion"] = df_merged["hrv_norm"] * 20
    
    df_merged["target"] = (
        df_merged["score_duracion"] +
        df_merged["score_calidad"] +
        df_merged["score_recuperacion"]
    )
    
    return df_merged

def obtener_modelo_entrenado():
    """Entrena y devuelve el modelo, imputer y columnas de entrenamiento"""
    df_merged = cargar_datos()
    
    cols_sueno = [
        'Análisis del Sueño [Total] (hr)', 'Análisis del Sueño [Core] (hr)',
        'Análisis del Sueño [Deep] (hr)', 'Análisis del Sueño [REM] (hr)', 
        'Análisis del Sueño [Awake] (hr)', 'fecha'
    ]
    X = df_merged.drop(columns=cols_sueno + ['target'], errors='ignore')
    y = df_merged['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)
    
    imputer = SimpleImputer(strategy='mean')
    X_train_imputed = imputer.fit_transform(X_train)
    
    mask_train = ~y_train.isna()
    X_train_imputed_clean = X_train_imputed[mask_train]
    y_train_clean = y_train[mask_train]

    reg = ElasticNet()
    reg.fit(X_train_imputed_clean, y_train_clean)
    
    return reg, imputer, X_train

