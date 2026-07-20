import streamlit as st
import pandas as pd
import yfinance as yf
import dd_motor as dd_calc  

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Simulador de Maximum Drawdown", layout="centered")

# --- 1. DESCARGA DE DATOS REALES ---
@st.cache_data(show_spinner=False)
def descargar_datos_prueba():
    datos = yf.download(["GOOGL", "META"], period="5y", progress=False)['Close']
    return datos.ffill()

datos_historicos = descargar_datos_prueba()

# --- 2. CONTROLES DEL PORTAFOLIO ---
st.subheader("1. Arma tu Portafolio")

col1, col2 = st.columns(2)
with col1:
    cant_googl = st.number_input("Acciones de Google (GOOGL)", min_value=0, value=0, step=1)
with col2:
    # Por defecto ponemos 10 a Meta para que puedas replicar fácilmente el -67% de la imagen
    cant_meta = st.number_input("Acciones de Meta (META)", min_value=0, value=10, step=1) 

# --- 3. PROCESAMIENTO Y RESULTADO VISUAL ---
if cant_googl == 0 and cant_meta == 0:
    st.warning("Añade al menos 1 acción para ver los resultados.")
else:
    # Cálculo
    valor_diario_portafolio = (datos_historicos['GOOGL'] * cant_googl) + (datos_historicos['META'] * cant_meta)
    max_dd = dd_calc.calcular_max_drawdown(valor_diario_portafolio)
    etiqueta, color = dd_calc.interpretar_drawdown(max_dd)

    st.divider()
    
    # Vista idéntica a la captura
    st.subheader("2. Resultados del Riesgo (Últimos 5 años)")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric(label="Maximum Drawdown Histórico", value=f"{max_dd * 100:.2f}%")
    with col_res2:
        if color == "green":
            st.success(f"**Nivel {etiqueta}:** Muy conservador.")
        elif color == "orange":
            st.warning(f"**Nivel {etiqueta}:** Riesgo normal de mercado.")
        elif color == "red":
            st.error(f"**Nivel {etiqueta}:** Caídas fuertes. Requiere estómago.")
        else:
            st.error(f"🚨 **Nivel {etiqueta}:** Riesgo extremo.")