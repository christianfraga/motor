import pandas as pd
import numpy as np

def calcular_metricas(datos, pesos_dict, anos=10):
    """
    Calcula CAGR, Volatilidad y Correlación de un portafolio.
    Resistente a huecos y asimetrías. Corregido con álgebra matricial.
    """
    if datos is None or datos.empty or not pesos_dict:
        return None, None, None

    activos_comunes = [t for t in pesos_dict.keys() if t in datos.columns]
    if not activos_comunes:
        return None, None, None

    # CORRECCIÓN: Operador de asignación agregado
    datos = datos[activos_comunes]

    # Normalizar los pesos (para que sumen exactamente 1.0)
    pesos_raw = np.array([pesos_dict[t] for t in activos_comunes])
    suma_pesos = pesos_raw.sum()
    if suma_pesos == 0:
        return 0.0, 0.0, 0.0
    pesos_norm = pesos_raw / suma_pesos

    # Filtrar por ventana de tiempo
    fecha_final = datos.index.max()
    fecha_inicial = fecha_final - pd.DateOffset(years=anos)
    datos_periodo = datos[datos.index >= fecha_inicial]

    # Calcular retornos aislando solo los días donde todos los activos seleccionados existen
    retornos = datos_periodo.pct_change().dropna(how='any')
    
    # Comprobación de flexibilidad (mínimo de días bursátiles cruzados para que la métrica tenga sentido)
    dias_comunes_reales = len(retornos)
    if dias_comunes_reales < 100: 
        return None, None, None

    # Retorno diario del portafolio 
    retornos_portafolio = retornos.dot(pesos_norm)

    # Métrica 1: CAGR (Rendimiento Anualizado Compuesto unificado con los retornos diarios)
    anos_reales = dias_comunes_reales / 252.0
    crecimiento_acumulado = (1 + retornos_portafolio).prod()
    cagr = (crecimiento_acumulado ** (1 / anos_reales)) - 1

    # Métrica 2: Volatilidad Anualizada
    volatilidad = retornos_portafolio.std() * np.sqrt(252)

    # Métrica 3: Correlación Interna Ponderada (Vectorizada con NumPy)
    if len(activos_comunes) > 1:
        matriz_corr = retornos.corr()
        w = pesos_norm
        suma_pesos_cuadrados = np.sum(w ** 2)
        
        # Fórmula matricial para evitar bucles for lentos
        if suma_pesos_cuadrados < 1.0:
            corr_ponderada = (w.T @ matriz_corr @ w - suma_pesos_cuadrados) / (1 - suma_pesos_cuadrados)
        else:
            corr_ponderada = 1.0
            
        correlacion = corr_ponderada
    else:
        correlacion = 1.0

    return cagr, volatilidad, correlacion