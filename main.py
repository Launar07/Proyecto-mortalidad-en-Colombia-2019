# Despliegue limpio v2 - Estructura completa
import streamlit as st
from controlador import MortalidadController
from vistas.graficos import renderizar_dashboard

# Configuración del entorno web
st.set_page_config(page_title="Mortalidad Colombia 2019", layout="wide")


# Instanciar el controlador global de la aplicación de manera persistente
if 'controlador' not in st.session_state:
    st.session_state.controlador = MortalidadController()

# Llamar directamente a la vista pasando nuestro controlador
renderizar_dashboard(st.session_state.controlador)
