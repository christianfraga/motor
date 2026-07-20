def calcular_sharpe(cagr, volatilidad, tasa_libre_riesgo=0.04):
    """
    Calcula el Ratio de Sharpe.
    Los parámetros deben ingresar como decimales (ej. 0.10 para 10%).
    """
    # Prevención de división por cero
    if volatilidad <= 0.0:
        return 0.0
    
    # Matemáticas del Sharpe Ratio
    exceso_retorno = cagr - tasa_libre_riesgo
    sharpe_ratio = exceso_retorno / volatilidad
    
    return sharpe_ratio

def interpretar_sharpe(sharpe_ratio):
    """
    Evalúa el número y devuelve una etiqueta y un color 
    para usar en la interfaz visual.
    """
    if sharpe_ratio < 0.50:
        return "Ineficiente", "red"
    elif sharpe_ratio < 1.00:
        return "Aceptable", "orange"
    elif sharpe_ratio < 2.00:
        return "Eficiente", "green"
    else:
        return "Excepcional", "blue"