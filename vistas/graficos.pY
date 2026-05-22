import streamlit as st
import plotly.express as px

def renderizar_dashboard(controlador):

    st.title("📊 Sistema de Análisis Estadístico de Mortalidad")
    # --- PARTE 1: SECCIÓN DE CARGA (Tus pestañas anteriores) ---
    st.subheader("📁 Centro de Carga y Gestión de Archivos")
    tab_c1, tab_c2, tab_c3 = st.tabs([
        "📊 Base Mortalidad", "🩺 Catálogo CIE-10", "🗺️ Divipola"
    ])
    
    with tab_c1:
        if st.button("🔄 Cargar Mortalidad", key="b1"): controlador.procesar_mortalidad()
        if controlador.df_mortalidad is not None: st.caption("Mortalidad cargada.")
    with tab_c2:
        if st.button("🔄 Cargar Catálogo", key="b2"): controlador.procesar_causas()
        if controlador.df_causas is not None: st.caption("Catálogo cargado.")
    with tab_c3:
        if st.button("🔄 Cargar Divipola", key="b3"): controlador.procesar_divipola()
        if controlador.df_divipola is not None: st.caption("Divipola cargada.")

    # --- PARTE 2: EL CUADRO DE REQUERIMIENTOS SOLICITADOS EN PESTAÑAS ---
    st.markdown("---")
    st.header("📈 Módulos de Visualización e Interpretación")
    
    # Validamos que los datos estén listos
    df_consolidado = controlador.obtener_datos_consolidados()
    
    if df_consolidado is None:
        st.warning("⚠️ Carga los 3 archivos en la sección superior para desbloquear las pestañas de gráficos.")
        return

    t1, t2, t3, t4, t5, t6, t7 = st.tabs([
        "🗺️ Mapa Departamental", 
        "📈 Línea Temporal (Meses)", 
        "🚨 Ciudades más Violentas", 
        "🟢 Menor Mortalidad", 
        "📋 Top 10 Causas", 
        "🚻 Análisis por Género",
        "⏳ Distribución por Edad" 
    ])

    # 1. TAB MAPA DEPARTAMENTAL
    with t1:
        st.subheader("Distribución Total de Muertes por Departamento (2019)")
        df_mapa = controlador.datos_mapa_departamental()
        
        # Gráfico de barras horizontal como alternativa limpia si no cuentas con GeoJSON de Colombia
        fig_mapa = px.bar(df_mapa, x='Total Muertes', y='DEPARTAMENTO', 
                          title="Frecuencia de Fallecimientos por Territorio",
                          orientation='h', color='Total Muertes',
                          color_continuous_scale='Reds')
        fig_mapa.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_mapa, use_container_width=True)
        st.info("💡 **Interpretación:** Los departamentos con mayor población (como Antioquia, Valle del Cauca o Bogotá D.C.) suelen concentrar el mayor volumen absoluto de muertes naturales y externas.")

    # 2. TAB GRÁFICO DE LÍNEAS (POR MES)
    with t2:
        st.subheader("Evolución del Total de Muertes por Mes")
        df_mes = controlador.datos_muertes_por_mes()
        
        fig_linea = px.line(df_mes, x='Nombre Mes', y='Total Muertes', 
                            title="Comportamiento del Volumen de Defunciones a lo largo del Año",
                            markers=True, line_shape="spline")
        st.plotly_chart(fig_linea, use_container_width=True)
        st.info("💡 **Interpretación:** Permite observar picos estacionales de mortalidad. Históricamente, diciembre y enero registran variaciones debido a incrementos en causas externas (accidentes/homicidios).")

    # 3. TAB GRÁFICO DE BARRAS (CIUDADES MÁS VIOLENTAS)
    with t3:
        st.subheader("Top 5 Municipios con Mayor Número de Homicidios")
        df_violencia = controlador.datos_ciudades_mas_violentas()
        
        fig_violencia = px.bar(df_violencia, x='Ciudad', y='Homicidios',
                               title="Ciudades Afectadas por Agresiones y Armas de Fuego (X95)",
                               color='Homicidios', color_continuous_scale='Purples')
        st.plotly_chart(fig_violencia, use_container_width=True)
        st.info("💡 **Interpretación:** Este gráfico aísla los casos clasificados estrictamente bajo el código CIE-10 enfocado en violencia por armas de fuego o agresiones directas, reflejando problemas de seguridad urbana.")

    # 4. TAB GRÁFICO CIRCULAR (MENOR MORTALIDAD)
    with t4:
        st.subheader("Top 10 Municipios con Menor Índice Absoluto de Mortalidad")
        df_menor = controlador.datos_ciudades_menor_mortalidad()
        
        fig_pie = px.pie(df_menor, values='Total Casos', names='Ciudad',
                         title="Distribución de Municipios con Menor Registro de Fallecidos")
        st.plotly_chart(fig_pie, use_container_width=True)
        st.info("💡 **Interpretación:** Representa los territorios con menor cantidad de decesos. Generalmente corresponde a corregimientos o áreas no municipalizadas con baja densidad demográfica.")

    # 5. TAB TABLA (TOP 10 CAUSAS DE MUERTE)
    with t5:
        st.subheader("Principales Causas de Muerte en Colombia")
        df_top_causas = controlador.datos_top_causas_muerte()
        
        # Mostramos la tabla formateada y estilizada
        st.dataframe(df_top_causas, use_container_width=True, hide_index=True)
        st.info("💡 **Interpretación:** Las enfermedades isquémicas del corazón y afecciones crónicas suelen ocupar los primeros puestos de esta lista de acuerdo a los estándares epidemiológicos del DANE.")

    # 6. TAB GRÁFICO DE BARRAS APILADAS (SEXO POR DEPARTAMENTO)
    with t6:
        st.subheader("Comparativa de Mortalidad por Sexo y Departamento")
        df_sexo = controlador.datos_mortalidad_por_sexo_depto()
        
        fig_apilado = px.bar(df_sexo, x='DEPARTAMENTO', y='Casos', color='Género',
                             title="Distribución de Defunciones por Género en el Territorio Nacional",
                             barmode='stack')
        st.plotly_chart(fig_apilado, use_container_width=True)
        st.info("💡 **Interpretación:** Evalúa diferencias significativas de género. En la mayoría de departamentos, la brecha de mortalidad masculina suele ser mayor debido a factores vinculados con causas de muerte externas (accidentes de tránsito y orden público).")

    with t7:
        st.subheader("⏳ Histograma de Distribución de Mortalidad por Etapas de Vida")
        st.markdown(
            "Visualización del volumen total de defunciones en Colombia agrupadas por "
            "rangos de edad bajo la codificación estandarizada del DANE."
        )
        
        # Llamamos al controlador para traer los datos agrupados y ordenados
        df_dist_edad = controlador.datos_distribucion_edad()
        
        if df_dist_edad is not None and not df_dist_edad.empty:
            # Creamos el gráfico de barras que simula el comportamiento del histograma de distribución
            fig_edad = px.bar(
                df_dist_edad, 
                x='Etapa de Vida', 
                y='Total Casos',
                title="Distribución Absoluta de Defunciones por Grupo Etario (2019)",
                color='Total Casos',
                color_continuous_scale='Blues',
                text_auto=',.0f' # Muestra los números encima de las barras formateados con miles
            )
            
            # Ajustes estéticos del gráfico
            fig_edad.update_layout(
                xaxis_title="Etapas de Desarrollo / Rangos de Edad",
                yaxis_title="Cantidad de Defunciones",
                xaxis_tickangle=-45, # Inclina las etiquetas para que no se traslapen
                showlegend=False
            )
            
            # Renderizar en Streamlit
            st.plotly_chart(fig_edad, use_container_width=True)
            
            # --- SECCIÓN DE INTERPRETACIÓN DE RESULTADOS EXIGIDA POR EL LABORATORIO ---
            st.info(
                "💡 **Interpretación de los Resultados:**\n\n"
                "El gráfico de distribución revela una curva epidemiológica característica en países en desarrollo. "
                "Se observa una concentración crítica de casos en las etapas de **Vejez** y **Adultez Intermedia**, "
                "lo cual es consistente con el envejecimiento natural de la población y enfermedades crónico-degenerativas.\n\n"
                "Por otra parte, el pico visible en la **Mortalidad neonatal / infantil** denota los retos del sistema de salud "
                "pública perinatal en las regiones colombianas durante el año analizado."
            )
        else:
            st.error("Error al procesar la distribución de variables de edad. Verifica que la columna GRUPO_EDAD1 contenga datos válidos.")