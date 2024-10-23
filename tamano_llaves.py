"""
DATOS DE LA BASE DE DATOS tornillos.db, TABLA tamano_llaves

El tamaño de las llaves se ha extraido de

https://en.wikipedia.org/wiki/ISO_metric_screw_thread

18/10/2024

__author__ = Pedro Biel

__version__ = 0.0.0

__email__ = pedro.biel@abalsirengineering.com
"""

import pandas as pd
from src.utils.paths import Paths
from src.utils.sqlitepandasdf import SQLitePandasDF


class DatosTamanoLlaves:

    def __init__(self) -> None:
        """
        Clase que gestiona los datos de la tabla 'tamano_llaves' de la base de datos 'tornillos.db'.
        Proporciona valores del diámetro nominal (dnom_mm) y del tamaño de la llave (s_mm) para las métricas indicadas.

        El tamaño de las llaves se ha extraido de

        https://en.wikipedia.org/wiki/ISO_metric_screw_thread

        Las métricas para las que se desconoce el tamaño de la llave se da el valor 0.
        """

        # Ruta a la base de datos de acero estructural
        self.ruta_datos = f'{Paths.data}\\'
        self.tornillos_db = 'tornillos.db'
        self.tabla = 'tamano_llaves'

        # Clase para gestionar la conexión a SQLite
        self.sql_pd = SQLitePandasDF

        # Cache para almacenar el DataFrame y evitar múltiples lecturas
        self._df_cache = None

    def _load_dataframe(self) -> pd.DataFrame:
        """
        Carga el DataFrame desde la base de datos SQLite y lo cachea para evitar múltiples accesos.

        :return: DataFrame con los datos de la tabla.
        """
        if self._df_cache is None:  # Solo carga el DataFrame si no está en cache
            sql_pd = self.sql_pd(f'{self.ruta_datos}{self.tornillos_db}', self.tabla)
            self._df_cache = sql_pd.sql_to_df()
        return self._df_cache

    def metricas(self) -> list[str]:
        """
        Obtiene la lista de métricas disponibles.

        :return: Lista de métricas (columna 'Metrica').
        """
        df = self._load_dataframe()
        return df['Métrica'].to_list()

    def diametros_nominales(self) -> list[float]:
        """
        Obtiene la lista de diámetros nominales (columna 'dnom_mm').

        :return: Lista de diámetros nominales en mm.
        """
        df = self._load_dataframe()
        return df['dnom_mm'].to_list()

    def diametro_nominal(self, metrica: str) -> float:
        """
        Obtiene el diámetro nominal en mm para una métrica específica.

        :param metrica: La métrica para la cual se desea obtener el diámetro nominal.
        :return: Diámetro nominal en mm.
        """
        df = self._load_dataframe()
        return df.loc[df['Métrica'] == metrica, 'dnom_mm'].item()

    def tamanos_llave(self) -> list[float]:
        """
        Obtiene la lista de los tamaños de llave (columna 's_mm').

        :return: Lista de diámetros nominales en mm.
        """
        df = self._load_dataframe()
        return df['s_mm'].to_list()

    def tamano_llave(self, metrica: str) -> float:
        """
        Obtiene el tamaño de llave en mm para una métrica específica.

        :param metrica: La métrica para la cual se desea obtener el diámetro nominal.
        :return: Diámetro nominal en mm.
        """
        df = self._load_dataframe()
        return df.loc[df['Métrica'] == metrica, 's_mm'].item()


if __name__ == '__main__':
    from prettytable import PrettyTable

    # Inicializa PrettyTable para mostrar los resultados
    tabla = PrettyTable()

    # Crea una instancia de DatosISODIN13
    datos = DatosTamanoLlaves()

    # Obtiene las métricas, diámetros nominales y pasos
    metricas = datos.metricas()
    diametros = datos.diametros_nominales()
    llaves = datos.tamanos_llave()

    # Añade las columnas a la tabla
    tabla.add_column('Métrica', metricas)
    tabla.add_column('Diámetro (mm)', diametros)
    tabla.add_column('Llave (mm)', llaves)

    # Imprime la tabla
    print(tabla)
