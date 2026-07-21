import pandas as pd
import yfinance as yf
import streamlit as st
import requests

@st.cache_data(ttl=3600, show_spinner=False)
def buscar_activos_yahoo_api(query):
    """Busca tickers y nombres de empresas en milisegundos."""
    if not query or len(query) < 2:
        return []
    try:
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=5"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=4).json()
        resultados = []
        for quote in res.get("quotes", []):
            ticker = quote.get("symbol")
            nombre = quote.get("longname") or quote.get("shortname") or "Activo Internacional"
            mercado = quote.get("exchange", "Global")
            if ticker:
                resultados.append({"ticker": ticker.upper(), "label": f"{ticker} - {nombre} ({mercado})"})
        return resultados
    except Exception:
        return []

@st.cache_data(ttl=600, show_spinner=False)
def obtener_precios_recientes(tickers):
    """Descarga solo los últimos días para mostrar el precio nominal en las tarjetas."""
    if not tickers:
        return {}
    try:
        datos = yf.download(tickers, period="5d", progress=False)['Close']
        if isinstance(datos, pd.Series):
            datos = datos.to_frame(name=tickers[0])
        # Rellenar hacia adelante para capturar el último cierre válido y evitar NaNs de hoy
        return datos.ffill().iloc[-1].to_dict()
    except Exception:
        return {t: 0.0 for t in tickers}

@st.cache_data(ttl=86400, show_spinner=False)
def descargar_datos_seguros(tickers, anos=10):
    """Descarga la historia completa ajustada para las matemáticas del motor."""
    if not tickers:
        return pd.DataFrame()
    try:
        # SOLUCIÓN: auto_adjust=True ajusta los dividendos y splits directamente en 'Close'
        # Esto evita que yfinance colapse al buscar columnas inexistentes.
        datos = yf.download(tickers, period="max", auto_adjust=True, progress=False)['Close']
        
        if isinstance(datos, pd.Series):
            datos = datos.to_frame(name=tickers[0])
            
        datos = datos.dropna(axis=1, how='all')
        datos = datos.ffill()
        return datos
    except Exception:
        return pd.DataFrame()