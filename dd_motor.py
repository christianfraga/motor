import pandas as pd
import numpy as np

def calcular_max_drawdown(serie_valores):
    """
    Calcula el Maximum Drawdown a partir de una serie de tiempo de precios/valores.
    Devuelve un float negativo (ejemplo: -0.25 representa un -25% de caída máxima).
    """
    if serie_valores is None or len(serie_valores) == 0:
        return 0.0
    
    # Asegurar que sea una serie de Pandas
    if not isinstance(serie_valores, pd.Series):
        serie_valores = pd.Series(serie_valores)
        
    # 1. Calcular el pico histórico acumulado hasta cada fecha
    picos = serie_valores.cummax()
    
    # 2. Calcular la caída porcentual respecto al pico acumulado
    drawdowns = (serie_valores - picos) / picos
    
    # 3. El Maximum Drawdown es el punto más bajo (mínimo) de la serie de caídas
    max_dd = drawdowns.min()
    
    return max_dd if not np.isnan(max_dd) else 0.0

def interpretar_drawdown(max_dd):
    """
    Clasifica el nivel de riesgo/dolor emocional según la profundidad de la caída.
    El parámetro max_dd entra como un decimal negativo (ej: -0.15 para -15%).
    """
    caida_pct = abs(max_dd) * 100
    
    if caida_pct <= 10.0:
        return "Bajo (Conservador)", "green"
    elif caida_pct <= 20.0:
        return "Moderado (Tolerable)", "orange"
    elif caida_pct <= 35.0:
        return "Alto (Volátil)", "red"
    else:
        return "Extremo (Peligro)", "purple"