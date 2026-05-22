import pandas as pd

class MortalidadController:
    def __init__(self, dataframe):
        self.df = dataframe

    def obtener_grilla_mortalidad(self):
        """Retorna las columnas clave ordenadas para la grilla interactiva"""
        columnas_interes = [
            'COD_DANE', 'DEPARTAMENTO', 'MUNICIPIO', 'SEXO', 
            'MES', 'COD_MUERTE', 'CAUSA_MUERTE_DESC', 'CATEGORIA_EDAD'
        ]
        # Devolvemos solo las columnas existentes para evitar caídas
        columnas_validas = [col for col in columnas_interes if col in self.df.columns]
        return self.df[columnas_validas]