import pandas as pd
import streamlit as st

@st.cache_data
def cargar_datos_mortalidad():
    """Carga y estandariza el archivo principal de defunciones sin fetos"""
    df = pd.read_excel("datos/Anexo1.NoFetal2019_CE_15-03-23 (1).xlsx", sheet_name="No_Fetales_2019")
    df.columns = df.columns.str.upper().str.strip()
    return df

@st.cache_data
def cargar_catalogo_causas():
    """Carga y limpia el catálogo CIE-10 usando las posiciones físicas de las columnas"""
    df = pd.read_excel("datos/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx")
    
    # Usar la fila 9 (índice 8) como nombres de columnas
    titulos = df.iloc[7, [2, 3, 4, 5]].astype(str).str.upper().str.strip().tolist()
    
    # Seleccionar datos desde la fila 10 (índice 9)
    df_limpio = df.iloc[8:, [2, 3, 4, 5]].copy()
    df_limpio.columns = titulos
    
    # Formatear textos y remover duplicados
    df_limpio = df_limpio.apply(lambda col: col.astype(str).str.upper().str.strip())
    df_limpio = df_limpio.drop_duplicates().reset_index(drop=True)
    return df_limpio

@st.cache_data
def cargar_datos_divipola():
    """Carga y estandariza los datos geográficos de Divipola"""
    df = pd.read_excel("datos/Divipola_CE_.xlsx", sheet_name="Hoja1")
    df.columns = df.columns.str.upper().str.strip()
    return df