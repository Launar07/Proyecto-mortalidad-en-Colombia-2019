import pandas as pd
import streamlit as st
import modelo 

class MortalidadController:
    def __init__(self):
        if 'df_mortalidad' not in st.session_state:
            st.session_state.df_mortalidad = None
        if 'df_causas' not in st.session_state:
            st.session_state.df_causas = None
        if 'df_divipola' not in st.session_state:
            st.session_state.df_divipola = None

    @property
    def df_mortalidad(self):
        return st.session_state.df_mortalidad

    @property
    def df_causas(self):
        return st.session_state.df_causas

    @property
    def df_divipola(self):
        return st.session_state.df_divipola

    def procesar_mortalidad(self):
        df = modelo.cargar_datos_mortalidad()
        st.session_state.df_mortalidad = df
        return df

    def procesar_causas(self):
        df = modelo.cargar_catalogo_causas()
        st.session_state.df_causas = df
        return df

    def procesar_divipola(self):
        df = modelo.cargar_datos_divipola()
        st.session_state.df_divipola = df
        return df

    # ==========================================
    # NUEVO MÉTODO: CONSOLIDACIÓN Y CRUCE DE DATOS
    # ==========================================
    def obtener_datos_consolidados(self):
        """
        Une la base de mortalidad con el catálogo CIE-10 y la Divipola.
        Asegura que los tipos de datos coincidan antes del cruce.
        """
        # Verificamos que las tres fuentes existan en memoria antes de cruzarlas
        if (st.session_state.df_mortalidad is None or 
            st.session_state.df_causas is None or 
            st.session_state.df_divipola is None):
            return None

        # 1. Copias de trabajo para evitar modificar los DataFrames originales
        mortalidad = st.session_state.df_mortalidad.copy()
        causas = st.session_state.df_causas.copy()
        divipola = st.session_state.df_divipola.copy()

        # Estandarizamos los tipos de datos de las llaves (keys) para que el merge no falle
        mortalidad['COD_MUERTE'] = mortalidad['COD_MUERTE'].astype(str).str.strip().str.upper()
        causas['CÓDIGO DE LA CIE-10 CUATRO CARACTERES'] = causas['CÓDIGO DE LA CIE-10 CUATRO CARACTERES'].astype(str).str.strip().str.upper()

        mortalidad['COD_DEPARTAMENTO'] = mortalidad['COD_DEPARTAMENTO'].astype(str).str.strip().str.upper()
        divipola['COD_DEPARTAMENTO'] = divipola['COD_DEPARTAMENTO'].astype(str).str.strip().str.upper()

        # 2. Primer Cruce: Mortalidad + Catálogo CIE-10 (Causas de muerte)
        # Usamos how='left' para no perder registros si algún código de muerte no está mapeado
        df_combinado = pd.merge(
            mortalidad, 
            causas, 
            left_on='COD_MUERTE', 
            right_on='CÓDIGO DE LA CIE-10 CUATRO CARACTERES', 
            how='left'
        )

        # 3. Segundo Cruce: El resultado anterior + Divipola (Departamentos)
        # Reducimos Divipola a códigos y nombres únicos de departamento para evitar duplicación de filas
        divipola_deptos = divipola[['COD_DEPARTAMENTO', 'DEPARTAMENTO']].drop_duplicates()
        
        df_final = pd.merge(
            df_combinado, 
            divipola_deptos, 
            on='COD_DEPARTAMENTO', 
            how='left'
        )

        return df_final

    # ==========================================
    # MÉTODOS PARA PROCESAR CADA GRÁFICO (MÓDULO DE ANÁLISIS)
    # ==========================================

    def datos_muertes_por_mes(self):
        df = self.obtener_datos_consolidados()
        if df is None or 'MES' not in df.columns: return None
        
        # Mapeo de números a nombres de meses
        meses_map = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        df_mes = df.groupby('MES').size().reset_index(name='Total Muertes')
        df_mes['Nombre Mes'] = df_mes['MES'].map(meses_map)
        return df_mes.sort_values('MES')

    def datos_ciudades_mas_violentas(self):
        df = self.obtener_datos_consolidados()
        if df is None or 'COD_MUERTE' not in df.columns: return None
        
        # Filtramos por homicidios específicos solicitados (ej: agresión con disparo, armas de fuego, etc.)
        # Nota: Puedes expandir la lista de códigos si es necesario (ej: X93, X94, X95, etc.)
        codigos_homicidio = ['X95', 'X950', 'X951', 'X952', 'X953', 'X954', 'X955', 'X956', 'X957', 'X958', 'X959']
        df_violencia = df[df['COD_MUERTE'].str.startswith('X95') | (df['MANERA_MUERTE'].str.upper() == 'HOMICIDIO')]
        
        # Agrupamos por Municipio (Usamos COD_DANE o MUNICIPIO si ya cruzaste municipios, o en su defecto COD_MUNICIPIO)
        # Para este ejemplo agrupamos por COD_DANE para ser exactos
        df_ciudades = df_violencia.groupby('COD_DANE').size().reset_index(name='Homicidios')
        
        # Cruzamos con Divipola para obtener el nombre real de la ciudad/municipio
        divipola = st.session_state.df_divipola[['COD_DANE', 'MUNICIPIO', 'DEPARTAMENTO']].drop_duplicates()
        df_ciudades = pd.merge(df_ciudades, divipola, on='COD_DANE', how='left')
        df_ciudades['Ciudad'] = df_ciudades['MUNICIPIO'] + " (" + df_ciudades['DEPARTAMENTO'] + ")"
        
        return df_ciudades.sort_values(by='Homicidios', ascending=False).head(5)

    def datos_ciudades_menor_mortalidad(self):
        df = self.obtener_datos_consolidados()
        if df is None: return None
        
        df_mortalidad = df.groupby('COD_DANE').size().reset_index(name='Total Casos')
        divipola = st.session_state.df_divipola[['COD_DANE', 'MUNICIPIO', 'DEPARTAMENTO']].drop_duplicates()
        df_mortalidad = pd.merge(df_mortalidad, divipola, on='COD_DANE', how='left')
        df_mortalidad['Ciudad'] = df_mortalidad['MUNICIPIO'] + " (" + df_mortalidad['DEPARTAMENTO'] + ")"
        
        # Las 10 ciudades con menor índice de mortalidad (menor número de casos)
        return df_mortalidad.sort_values(by='Total Casos', ascending=True).head(10)

    def datos_top_causas_muerte(self):
        df = self.obtener_datos_consolidados()
        if df is None: return None
        
        col_desc = 'DESCRIPCION  DE CÓDIGOS MORTALIDAD A CUATRO CARACTERES'
        df_causas = df.groupby(['COD_MUERTE', col_desc]).size().reset_index(name='Total Casos')
        df_causas.columns = ['Código CIE-10', 'Causa de Muerte', 'Total Casos']
        
        return df_causas.sort_values(by='Total Casos', ascending=False).head(10).reset_index(drop=True)

    def datos_mortalidad_por_sexo_depto(self):
        df = self.obtener_datos_consolidados()
        if df is None or 'DEPARTAMENTO' not in df.columns: return None
        
        # Mapeo de sexo (1: Masculino, 2: Femenino, o como venga en tu dataset)
        sexo_map = {1: 'Masculino', 2: 'Femenino', 3: 'Indeterminado', '1': 'Masculino', '2': 'Femenino'}
        df_copia = df.copy()
        df_copia['Género'] = df_copia['SEXO'].map(sexo_map).fillna('No Registrado')
        
        df_sexo = df_copia.groupby(['DEPARTAMENTO', 'Género']).size().reset_index(name='Casos')
        return df_sexo

    def datos_mapa_departamental(self):
        df = self.obtener_datos_consolidados()
        if df is None or 'DEPARTAMENTO' not in df.columns: return None
        
        df_mapa = df.groupby('DEPARTAMENTO').size().reset_index(name='Total Muertes')
        return df_mapa

    def datos_distribucion_edad(self):
        df = self.obtener_datos_consolidados()
        if df is None or 'GRUPO_EDAD1' not in df.columns: return None
        
        # 1. Creamos una copia para no alterar los datos originales
        df_edad = df.copy()
        
        # Aseguramos que la columna sea de tipo entero para evitar fallos de coincidencia
        df_edad['GRUPO_EDAD1'] = pd.to_numeric(df_edad['GRUPO_EDAD1'], errors='coerce')
        
        # 2. Definición de la función de mapeo según las categorías solicitadas
        def agrupar_etapa_vida(codigo):
            if codigo in [0, 1, 2, 3]: # Códigos DANE para menores de 1 año (días/meses)
                # Dependiendo de tu dataset, ajusta si vienen agrupados o desagregados
                if codigo in [1, 2]: return 'Mortalidad neonatal'
                return 'Mortalidad infantil'
            elif codigo in [4, 5, 6]:
                return 'Primera infancia'
            elif codigo in [7, 8]:
                return 'Niñez'
            elif codigo in [9, 10]:
                return 'Adolescencia'
            elif codigo in [11]:
                return 'Juventud'
            elif codigo in [12, 13, 14]: # 12 a 13 Adultez temprana (se incluye 14 según distribución estándar)
                return 'Adultez temprana'
            elif codigo in [15, 16, 17, 18, 19]: # 14-16 y 17-19 Adultez intermedia
                return 'Adultez intermedia'
            elif codigo in [20, 21, 22, 23, 24]:
                return 'Vejez'
            elif codigo in [25, 26, 27, 28]:
                return 'Longevidad / Centenarios'
            elif codigo == 29:
                return 'Edad desconocida'
            else:
                return 'Edad desconocida'

        # 3. Aplicamos el mapeo para crear la nueva columna categórica
        df_edad['Etapa de Vida'] = df_edad['GRUPO_EDAD1'].apply(agrupar_etapa_vida)
        
        # 4. Agrupamos y contamos las muertes por cada etapa
        df_resultado = df_edad.groupby('Etapa de Vida').size().reset_index(name='Total Casos')
        
        # 5. Definimos el orden lógico cronológico de las categorías para el gráfico
        orden_cronologico = [
            'Mortalidad neonatal',
            'Mortalidad infantil',
            'Primera infancia',
            'Niñez',
            'Adolescencia',
            'Juventud',
            'Adultez temprana',
            'Adultez intermedia',
            'Vejez',
            'Longevidad / Centenarios',
            'Edad desconocida'
        ]
        
        # Convertimos la columna en un tipo categórico ordenado de Pandas
        df_resultado['Etapa de Vida'] = pd.Categorical(
            df_resultado['Etapa de Vida'], 
            categories=orden_cronologico, 
            ordered=True
        )
        
        # Ordenamos el DataFrame final acorde a la estructura biológica
        return df_resultado.sort_values('Etapa de Vida')