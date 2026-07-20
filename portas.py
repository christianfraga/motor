import streamlit as st

# Configuración de página
st.set_page_config(
    page_title="Gestor de Portafolios",
    page_icon="📁",
    layout="wide"
)

# -----------------------------------------------------------------------------
# 1. BASE DE DATOS DE PORTAFOLIOS GUARDADOS
# -----------------------------------------------------------------------------
PORTAFOLIOS_PREDEFINIDOS = {
    "Christian": {
        "nombre": "Portafolio Christian",
        "subtitulo": "Estrategia de Crecimiento Tecnológico",
        "descripcion": "Alta concentración en Megacaps Tech (MSFT, META, GOOGL, AMZN) y AXP. Mayor volatilidad y retorno impulsado por sector IT.",
        "etiqueta": "Concentrado / Alto Riesgo",
        "color_etiqueta": "#FF4B4B",  # Rojo / Alerta
        "activos": {
            "MSFT": 4.0,
            "META": 3.0,
            "GOOGL": 2.0,
            "AMZN": 2.0,
            "AXP": 1.0
        }
    },
    "Optimizado_Sharpe_1.13": {
        "nombre": "Optimizado Sharpe 1.13",
        "subtitulo": "Estructura Defensiva & Diversificada",
        "descripcion": "Distribución 'Core & Satellite' descorrelacionada. Combina VOO, Dividendo (SCHD), Bonos (BND), Oro (GLD) y Tech seleccionada.",
        "etiqueta": "Defensivo / Eficiente",
        "color_etiqueta": "#00C853",  # Verde / Seguro
        "activos": {
            "VOO": 8.0,
            "SCHD": 31.0,
            "BND": 14.0,
            "GLD": 4.0,
            "MSFT": 2.0,
            "GOOGL": 4.0
        }
    }
}

# -----------------------------------------------------------------------------
# 2. INICIALIZACIÓN DEL ESTADO (session_state)
# -----------------------------------------------------------------------------
if "activos_activos" not in st.session_state:
    # Carga inicial por defecto: Portafolio Christian
    st.session_state["activos_activos"] = PORTAFOLIOS_PREDEFINIDOS["Christian"]["activos"].copy()

# -----------------------------------------------------------------------------
# 3. FUNCIÓN CALLBACK PARA CARGAR PRESET
# -----------------------------------------------------------------------------
def cargar_preset(clave_preset: str):
    """Sobreescribe los activos actuales con el preset seleccionado."""
    if clave_preset in PORTAFOLIOS_PREDEFINIDOS:
        st.session_state["activos_activos"] = PORTAFOLIOS_PREDEFINIDOS[clave_preset]["activos"].copy()
        st.toast(f"✅ Portafolio **{PORTAFOLIOS_PREDEFINIDOS[clave_preset]['nombre']}** cargado con éxito.", icon="🚀")

# -----------------------------------------------------------------------------
# 4. COMPONENTE VISUAL: SECCIÓN DE PORTAFOLIOS GUARDADOS
# -----------------------------------------------------------------------------
def render_gestor_portafolios():
    """Renderiza la sección UI de presets almacenados."""
    st.markdown("---")
    st.markdown("### 📁 Portafolios Guardados")
    st.caption("Selecciona una plantilla para reestructurar automáticamente tu estrategia de inversión.")

    cols = st.columns(len(PORTAFOLIOS_PREDEFINIDOS))

    for idx, (key, preset) in enumerate(PORTAFOLIOS_PREDEFINIDOS.items()):
        with cols[idx]:
            # Contenedor estilo tarjeta
            with st.container(border=True):
                # Encabezado de tarjeta
                st.markdown(f"#### {preset['nombre']}")
                st.caption(preset["subtitulo"])
                
                # Badge de categoría
                st.markdown(
                    f"<span style='background-color:{preset['color_etiqueta']}22; color:{preset['color_etiqueta']}; "
                    f"padding:3px 8px; border-radius:12px; font-size:0.8rem; font-weight:bold; border: 1px solid {preset['color_etiqueta']}'>"
                    f"{preset['etiqueta']}</span>",
                    unsafe_allow_html=True
                )
                
                st.write("") # Espaciador
                st.write(preset["descripcion"])
                
                # Desglose rápido de activos en código
                desglose_txt = " • ".join([f"**{ticker}**: {partes}" for ticker, partes in preset["activos"].items()])
                st.markdown(f"> **Composición:** {desglose_txt}")
                
                st.write("") # Espaciador
                
                # Botón de Carga
                st.button(
                    label=f"📥 Cargar {preset['nombre']}",
                    key=f"btn_load_{key}",
                    use_container_width=True,
                    type="primary" if key == "Optimizado_Sharpe_1.13" else "secondary",
                    on_click=cargar_preset,
                    args=(key,)
                )

# -----------------------------------------------------------------------------
# 5. DEMOSTRACIÓN DE ESTADO ACTUAL (SIMULACIÓN DE LA APP)
# -----------------------------------------------------------------------------
st.title("🧪 Demo: Gestor de Presets de Portafolio")

st.markdown("#### 🎯 Estado Actual del Portafolio (`st.session_state`)")
st.info("Esta sección simula lo que tu app principal (`porta.py`) leerá para hacer sus cálculos matemáticos.")

# Mostrar activos cargados actualmente
st.json(st.session_state["activos_activos"])

# Renderizar la nueva sección abajo
render_gestor_portafolios()