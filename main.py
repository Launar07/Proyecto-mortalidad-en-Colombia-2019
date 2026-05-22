
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from modelo import cargar_y_limpiar_datos
from controlador import MortalidadController
from vistas.graficos import renderizar_dashboard

# Configuración inicial de la App
st.set_page_config(page_title="App Mortalidad Colombia", layout="wide")

st.title("📊 Sistema de Análisis de Mortalidad - Colombia 2019")
st.markdown("Análisis desarrollado bajo arquitectura de software **MVC**.")

# Inicializar el Modelo mediante caché de Streamlit
@st.cache_data
def inicializar_datos():
    return cargar_y_limpiar_datos()

try:
    # 1. Cargar datos (MODELO)
    df_procesado = inicializar_datos()
    
    # 2. Instanciar el CONTROLADOR
    controlador = MortalidadController(df_procesado)
    
    # 3. Enviar el controlador a la VISTA para pintar los gráficos
    renderizar_dashboard(controlador)

except Exception as e:
    st.error(f"Error crítico en la ejecución del sistema: {e}")