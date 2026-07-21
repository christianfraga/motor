import streamlit as st
import pandas as pd
import motor
import plotly.express as px
from datos import buscar_activos_yahoo_api, obtener_precios_recientes, descargar_datos_seguros

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Terminal de Diagnóstico Financiero", page_icon="📈", layout="wide")

# --- MEMORIA INICIAL ---
if 'mi_portafolio' not in st.session_state: 
    st.session_state.mi_portafolio = {"MSFT": 4.0, "META": 3.0, "GOOGL": 2.0, "AMZN": 2.0, "AXP": 1.0}
if 'nombres_activos' not in st.session_state: 
    st.session_state.nombres_activos = {
        "MSFT": "Microsoft Corporation", "META": "Meta Platforms", "GOOGL": "Alphabet Inc.",
        "AMZN": "Amazon.com", "AXP": "American Express" 
    }

st.title("📈 Diagnóstico Estratégico de Portafolio") 
st.markdown("Simulación de riesgo, correlación y caídas máximas en tiempo real.") 
st.divider()

# --- 1. ZONA DE BÚSQUEDA Y COMPRA ---
st.subheader("1. Buscar y Añadir Activos") 
with st.container(border=True): 
    c1, c2 = st.columns([2, 1], vertical_alignment="bottom") 
    with c1: 
        busqueda = st.text_input("Ingresa ticker o empresa:", value="", label_visibility="collapsed", placeholder="Ejemplo: Tesla, AAPL, VOO...") 
    with c2:
        st.caption("🔍 Busca para añadir cobertura al portafolio")

    if busqueda:
        resultados = buscar_activos_yahoo_api(busqueda)
        if resultados:
            opciones = {res['label']: res for res in resultados}
            seleccion_label = st.selectbox("Confirmar activo:", list(opciones.keys()))
            ticker_sel = opciones[seleccion_label]['ticker']
            
            if st.button(f"➕ Añadir {ticker_sel} al portafolio", type="primary"):
                partes_label = opciones[seleccion_label]['label'].split(" - ")
                nombre_extraido = partes_label[1] if len(partes_label) > 1 else partes_label[0]
                st.session_state.nombres_activos[ticker_sel] = nombre_extraido
                
                if ticker_sel not in st.session_state.mi_portafolio:
                    st.session_state.mi_portafolio[ticker_sel] = 1.0
                st.rerun()
        else:
            st.warning("No se encontraron coincidencias.")

st.write("")

if st.session_state.mi_portafolio: 
    mis_tickers = list(st.session_state.mi_portafolio.keys())
    
    with st.spinner("Sincronizando cotizaciones y algoritmos matemáticos..."):
        precios_vivo = obtener_precios_recientes(mis_tickers)
        df_historico = descargar_datos_seguros(mis_tickers, anos=10)

    # --- 2. ZONA DEL PORTAFOLIO ---
    st.subheader("2. Composición de tu Portafolio")
    st.caption("Ajusta las cantidades de los activos actuales. Los cálculos se actualizarán automáticamente.")

    def actualizar_cantidad(ticker_mod):
        st.session_state.mi_portafolio[ticker_mod] = st.session_state[f"cant_{ticker_mod}"]

    filas_de_activos = [mis_tickers[i:i + 5] for i in range(0, len(mis_tickers), 5)]
    
    for fila in filas_de_activos:
        cols = st.columns(5)
        for idx, ticker in enumerate(fila):
            cantidad_actual = st.session_state.mi_portafolio[ticker]
            precio_actual = precios_vivo.get(ticker, 0.0)
            
            with cols[idx]:
                with st.container(border=True):
                    c_top1, c_top2 = st.columns([3, 1])
                    with c_top1:
                        st.markdown(f"**{ticker}**")
                    with c_top2:
                        if st.button("X", key=f"del_{ticker}", help="Eliminar", use_container_width=True):
                            del st.session_state.mi_portafolio[ticker]
                            st.rerun()
                    
                    if precio_actual == 0.0:
                        st.error("Sin cotización")
                    else:
                        st.markdown(f"<span style='color:#2e7d32; font-size:16px; font-weight:600;'>${precio_actual:,.2f} USD</span>", unsafe_allow_html=True)
                    
                    nombre_mostrar = st.session_state.nombres_activos.get(ticker, ticker)
                    st.caption(nombre_mostrar[:25])
                    
                    st.number_input(
                        "Partes",
                        value=float(cantidad_actual),
                        min_value=0.0,
                        step=1.0,
                        key=f"cant_{ticker}",
                        label_visibility="collapsed",
                        on_change=actualizar_cantidad,
                        args=(ticker,)
                    )

    valor_total = sum([cant * precios_vivo.get(t, 0.0) for t, cant in st.session_state.mi_portafolio.items()])
    pesos_monetarios = {t: (cant * precios_vivo.get(t, 0.0)) / valor_total for t, cant in st.session_state.mi_portafolio.items()} if valor_total > 0 else {}
    
    st.write("")
    st.divider()
    
    # --- 2.1 PORTAFOLIOS GUARDADOS ---
    st.subheader("2.1 Cargar Portafolio Guardado")
    st.caption("Sobrescribe tu portafolio actual con plantillas rápidas.")
    
    col_btn1, col_btn2, _ = st.columns([1, 1, 4])
    
    with col_btn1:
        if st.button("👤 Christian", use_container_width=True):
            st.session_state.mi_portafolio = {
                "MSFT": 4.0, "META": 3.0, "GOOGL": 2.0, "AMZN": 2.0, "AXP": 1.0
            }
            st.session_state.nombres_activos.update({
                "MSFT": "Microsoft Corporation", "META": "Meta Platforms", 
                "GOOGL": "Alphabet Inc.", "AMZN": "Amazon.com", "AXP": "American Express"
            })
            st.rerun()
            
    with col_btn2:
        if st.button("⚡ Optimizado", use_container_width=True):
            st.session_state.mi_portafolio = {
                "VOO": 8.0, "SCHD": 31.0, "BND": 14.0, "GLD": 4.0, "MSFT": 2.0, "GOOGL": 4.0
            }
            st.session_state.nombres_activos.update({
                "VOO": "Vanguard S&P 500 ETF", "SCHD": "Schwab US Dividend Equity ETF", 
                "BND": "Vanguard Total Bond Market ETF", "GLD": "SPDR Gold Trust",
                "MSFT": "Microsoft Corporation", "GOOGL": "Alphabet Inc."
            })
            st.rerun()
            
    st.write("")
    st.divider()

    # --- 3. ZONA DE MATEMÁTICAS Y DIAGNÓSTICO ---
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        st.subheader("3. Matemáticas y Diagnóstico de Riesgo")
    with col_t2:
        rf_pct = st.number_input("Tasa Libre de Riesgo (%)", value=4.0, step=0.25)
        rf_decimal = rf_pct / 100

    if valor_total > 0:
        col_grafico, col_metricas = st.columns([1.2, 3], gap="large")
        
        with col_grafico:
            st.metric(label="PATRIMONIO TOTAL", value=f"${valor_total:,.2f} USD")
            df_pesos = pd.DataFrame({
                "Activo": list(pesos_monetarios.keys()),
                "Porcentaje": [p * 100 for p in pesos_monetarios.values()]
            })
            fig = px.pie(df_pesos, values="Porcentaje", names="Activo", hole=0.7, color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_traces(textinfo="none", hovertemplate="<b>%{label}</b>: %{value:.1f}%<extra></extra>")
            fig.update_layout(
                showlegend=True, margin=dict(t=10, b=0, l=0, r=0), height=230,
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            
        with col_metricas:
            tab2, tab5, tab10 = st.tabs(["2 Años", "5 Años", "10 Años"])
            
            for ventana, tab in {2: tab2, 5: tab5, 10: tab10}.items():
                with tab:
                    # Llama al motor pasando correctamente la tasa libre de riesgo
                    rend, vol, corr, max_dd, sharpe = motor.calcular_metricas(
                        datos=df_historico, 
                        pesos_dict=pesos_monetarios, 
                        anos=ventana, 
                        tasa_libre_riesgo=rf_decimal
                    )
                    
                    if rend is not None and vol is not None:
                        # Colores Sharpe
                        if sharpe < 0.50: color_sh = "#ff4b4b"      # Rojo
                        elif sharpe < 1.00: color_sh = "gray"       # Gris
                        elif sharpe < 2.00: color_sh = "#21c354"    # Verde
                        else: color_sh = "#1c83e1"                  # Azul

                        # Colores Drawdown
                        caida_pct = abs(max_dd) * 100
                        if caida_pct <= 10.0: color_dd = "#21c354"   # Verde
                        elif caida_pct <= 20.0: color_dd = "gray"    # Gris
                        else: color_dd = "#ff4b4b"                  # Rojo

                        with st.container(border=True):
                            m1, m2, m3, m4, m5 = st.columns(5)
                            
                            m1.metric(label="Rendimiento", value=f"{rend * 100:.2f}%")
                            m2.metric(label="Volatilidad", value=f"{vol * 100:.2f}%")
                            
                            if len(mis_tickers) > 1 and corr is not None:
                                m3.metric(label="Correlación", value=f"{corr:.2f}")
                            else:
                                m3.info(">1 activo")
                                
                            estilo_label = "font-size: 14px; color: rgb(163, 168, 184); margin-bottom: 0px;"
                            estilo_valor = "font-size: 1.8rem; font-weight: 600; line-height: 1.2;"

                            m4.markdown(f"<div style='{estilo_label}'>Sharpe</div><div style='{estilo_valor} color: {color_sh};'>{sharpe:.2f}</div>", unsafe_allow_html=True)
                            m5.markdown(f"<div style='{estilo_label}'>Max Drawdown</div><div style='{estilo_valor} color: {color_dd};'>{max_dd * 100:.2f}%</div>", unsafe_allow_html=True)

                        # --- Dictamen Analítico ---
                        st.markdown("#### 🧠 Dictamen Analítico")
                        if len(mis_tickers) > 1 and corr is not None:
                            if corr > 0.70:
                                st.error("🚨 **ALERTA DE SOBREEXPOSICIÓN:** Activos altamente correlacionados. Urgente añadir cobertura (ej. Bonos, Oro).")
                            elif corr <= 0.39:
                                st.success("✅ **ESTRUCTURA DEFENSIVA:** Excelente distribución de riesgo. Activos descorrelacionados.")
                            else:
                                st.warning("⚠️ Correlación en niveles medios de mercado. Se puede mejorar la diversificación.")

                    else:
                        st.warning(f"📉 Historial común insuficiente en la ventana de {ventana} años.")
    else:
        st.info("💡 Asigna al menos 1 parte a tus activos para visualizar las métricas y el dictamen.")
else: 
    st.info("👋 El portafolio está vacío. Usa el buscador superior para comenzar.")