import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import time
from datetime import datetime, timedelta

# Configuración inicial de la página
st.set_page_config(page_title="Dashboard Financiero", layout="wide")

# Título de la aplicación
st.title("📊 Dashboard Financiero Pro")

# Sidebar para inputs del usuario
with st.sidebar:
    st.header("Configuración")
    ticker = st.text_input("Símbolo del ticker (ej. AAPL):", "AAPL")
    start_date = st.date_input("Fecha de inicio:", datetime.now() - timedelta(days=365))
    end_date = st.date_input("Fecha de fin:", datetime.now())
    interval = st.selectbox("Intervalo:", ['1d', '1wk', '1mo'])

# Función para obtener datos
@st.cache_data
def get_data(ticker, start, end, interval):
    try:
        data = yf.download(ticker, start=start, end=end, interval=interval)
        return data
    except Exception as e:
        st.error(f"Error al obtener datos: {e}")
        return None

# Obtener y mostrar datos
if st.button("Cargar Datos"):
    with st.spinner("Obteniendo datos financieros..."):
        df = get_data(ticker, start_date, end_date, interval)
        
        if df is not None and not df.empty:
            st.success("Datos cargados exitosamente!")
            
            # Mostrar datos
            st.subheader(f"Datos históricos para {ticker}")
            st.dataframe(df.style.highlight_max(axis=0), width=1000)
            
            # Gráfico de precios
            st.subheader("Evolución del precio de cierre")
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.lineplot(data=df, x=df.index, y='Close', ax=ax)
            ax.set_title(f"Precio de {ticker} ({start_date} a {end_date})")
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Precio de cierre (USD)")
            st.pyplot(fig)
            
            # Estadísticas
            st.subheader("Estadísticas clave")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Precio actual", f"${df['Close'].iloc[-1]:.2f}")
            with col2:
                st.metric("Cambio 7 días", f"${df['Close'].iloc[-1] - df['Close'].iloc[-7]:.2f}")
            with col3:
                st.metric("Volumen promedio", f"{df['Volume'].mean():,.0f}")
            
        else:
            st.warning("No se encontraron datos para el ticker especificado.")

# Notas adicionales
st.markdown("---")
st.info("""
**Notas:**
- Los datos se obtienen de Yahoo Finance usando la biblioteca yfinance
- Para actualizar los datos, haz clic en el botón 'Cargar Datos'
- Puedes cambiar el símbolo del ticker (ej. AAPL, MSFT, TSLA, etc.)
""")
