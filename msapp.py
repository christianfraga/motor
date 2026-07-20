import streamlit as st
import calculadora_sharpe as calc # Importamos tu nuevo archivo de lógica

# Configuración de la página
st.set_page_config(page_title="Prueba de Sharpe Ratio", layout="centered")

st.title("Calculadora de Sharpe Ratio")
st.write("Entorno de pruebas básico para validar el algoritmo antes de integrarlo al motor.")

st.divider()

# --- 1. ENTRADA DE DATOS ---
st.subheader("1. Configura los parámetros")

col1, col2, col3 = st.columns(3)

with col1:
    # CAGR del portafolio (Ej: 15%)
    cagr_pct = st.number_input("Rendimiento (CAGR %)", value=15.0, step=1.0)

with col2:
    # Volatilidad del portafolio (Ej: 20%)
    vol_pct = st.number_input("Riesgo (Volatilidad %)", value=20.0, step=1.0)

with col3:
    # Tasa Libre de Riesgo configurable (Por defecto 4%)
    rf_pct = st.number_input("Tasa Libre de Riesgo (%)", value=4.0, step=0.25)

# --- 2. PROCESAMIENTO ---
# Convertimos los porcentajes a decimales dividiendo entre 100
cagr_decimal = cagr_pct / 100
vol_decimal = vol_pct / 100
rf_decimal = rf_pct / 100

# Llamamos a nuestras funciones creadas en el otro archivo
mi_sharpe = calc.calcular_sharpe(cagr=cagr_decimal, volatilidad=vol_decimal, tasa_libre_riesgo=rf_decimal)
etiqueta, color = calc.interpretar_sharpe(mi_sharpe)

# --- 3. RESULTADOS VISUALES ---
st.divider()
st.subheader("2. Resultado y Dictamen")

st.metric(label="Ratio de Sharpe", value=f"{mi_sharpe:.2f}")

# Mostrar una alerta visual dependiendo del color que devolvió la función
if color == "red":
    st.error(f"**{etiqueta}:** El riesgo asumido es demasiado alto para el premio obtenido. Mejor dejar el dinero en renta fija.")
elif color == "orange":
    st.warning(f"**{etiqueta}:** El portafolio genera retornos, pero con mucha volatilidad. Hay margen de mejora.")
elif color == "green":
    st.success(f"**{etiqueta}:** ¡Excelente relación rendimiento/riesgo! El portafolio compensa muy bien la volatilidad.")
elif color == "blue":
    st.info(f"**{etiqueta}:** Gestión de riesgo fuera de lo común. (Nota: Ratios tan altos son difíciles de sostener a largo plazo).")