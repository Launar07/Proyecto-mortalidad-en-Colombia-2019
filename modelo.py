import pandas as pd

def cargar_y_limpiar_datos():
    # 1. Cargar los archivos usando tus hojas exactas
    df_mortalidad = pd.read_excel("datos/Anexo1.NoFetal2019_CE_15-03-23 (1).xlsx", sheet_name="No_Fetales_2019")
    df_causas = pd.read_excel("datos/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx")
    df_divipola = pd.read_excel("datos/Divipola_CE_.xlsx", sheet_name="Hoja1")

    # 2. Estandarizar columnas a mayúsculas y quitar espacios invisibles
    df_mortalidad.columns = df_mortalidad.columns.str.upper().str.strip()
    df_causas.columns = df_causas.columns.str.upper().str.strip()
    df_divipola.columns = df_divipola.columns.str.upper().str.strip()

    # 3. Limpieza de llaves para el Catálogo de Muerte (CIE-10 de 3 caracteres)
    # Extraemos los primeros 3 caracteres del código de muerte para asegurar el cruce perfecto
    df_mortalidad['COD_MUERTE_3'] = df_mortalidad['COD_MUERTE'].astype(str).str.strip().str.upper().str[:3]
    df_causas['COD_CIE3'] = df_causas['CÓDIGO DE LA CIE-10 TRES CARACTERES'].astype(str).str.strip().str.upper()

    # Eliminar duplicados del catálogo de causas para no duplicar filas en el cruce
    df_causas_unicas = df_causas.drop_duplicates(subset=['COD_CIE3']).copy()

    # 4. Unificar Mortalidad con Catálogo de Patologías
    df_completo = df_mortalidad.merge(
        df_causas_unicas[['COD_CIE3', 'DESCRIPCIÓN  DE CÓDIGOS MORTALIDAD A TRES CARACTERES']], 
        left_on='COD_MUERTE_3', 
        right_on='COD_CIE3', 
        how='left'
    )
    
    # Renombrar la columna larga de descripción a algo más cómodo
    if 'DESCRIPCIÓN  DE CÓDIGOS MORTALIDAD A TRES CARACTERES' in df_completo.columns:
        df_completo = df_completo.rename(columns={'DESCRIPCIÓN  DE CÓDIGOS MORTALIDAD A TRES CARACTERES': 'CAUSA_MUERTE_DESC'})

    # 5. Unificar con Divipola (Cruzando por el código DANE del Municipio)
    df_completo['COD_DANE'] = pd.to_numeric(df_completo['COD_DANE'], errors='coerce')
    df_divipola['COD_DANE'] = pd.to_numeric(df_divipola['COD_DANE'], errors='coerce')
    
    df_completo = df_completo.merge(
        df_divipola[['COD_DANE', 'DEPARTAMENTO', 'MUNICIPIO']], 
        on='COD_DANE', 
        how='left'
    )

    # 6. Mapeo estricto de grupos de edad exigidos por el laboratorio
    mapeo_edades = {
        0: 'Mortalidad neonatal', 1: 'Mortalidad neonatal', 2: 'Mortalidad neonatal', 
        3: 'Mortalidad neonatal', 4: 'Mortalidad neonatal',
        5: 'Mortalidad infantil', 6: 'Mortalidad infantil',
        7: 'Primera infancia', 8: 'Primera infancia',
        9: 'Niñez', 10: 'Niñez',
        11: 'Adolescencia',
        12: 'Juventud', 13: 'Juventud',
        14: 'Adultez temprana', 15: 'Adultez temprana', 16: 'Adultez temprana',
        17: 'Adultez intermedia', 18: 'Adultez intermedia', 19: 'Adultez intermedia',
        20: 'Vejez', 21: 'Vejez', 22: 'Vejez', 23: 'Vejez', 24: 'Vejez',
        25: 'Longevidad / Centenarios', 26: 'Longevidad / Centenarios', 
        27: 'Longevidad / Centenarios', 28: 'Longevidad / Centenarios',
        29: 'Edad desconocida'
    }
    
    if 'GRUPO_EDAD1' in df_completo.columns:
        df_completo['GRUPO_EDAD1_NUM'] = pd.to_numeric(df_completo['GRUPO_EDAD1'], errors='coerce')
        df_completo['CATEGORIA_EDAD'] = df_completo['GRUPO_EDAD1_NUM'].map(mapeo_edades).fillna('Edad desconocida')

    return df_completo