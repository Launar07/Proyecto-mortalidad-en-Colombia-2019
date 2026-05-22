import streamlit as st

def renderizar_dashboard(controlador):
    st.subheader("📋 Registro de Defunciones (Grilla de Datos)")
    
    # Obtener los datos limpios desde el controlador
    df_grilla = controlador.obtener_grilla_mortalidad()
    
    # Muestra el indicador superior
    total_registros = df_grilla.shape[0]
    st.metric(label="Total de Casos Procesados", value=f"{total_registros:,}")
    
    # Renderiza la tabla interactiva
    st.dataframe(df_grilla, use_container_width=True, height=400)
    st.caption("💡 Puedes hacer clic en las columnas para ordenar los datos geográficos o médicos.")