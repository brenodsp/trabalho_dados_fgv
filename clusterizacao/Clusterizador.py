from base_de_dados.DadosBase import DadosBase
from coletores.enums import GrupoMetricasEnum

import datetime

import pandas as pd
import sklearn.cluster as skl_cluster


class Clusterizador:
    _PESO_ENDIVIDAMENTO = 10
    _PESO_LIQUIDEZ = 7
    _PESO_ESCALA = 1
    def __init__(self, dados: DadosBase):
        self._dados = dados.df.set_index('NOME_EMPRESA')

    def clusterizar(self, num_clusters: int, estado_randomico: int = 42) -> pd.DataFrame:
        print(f"[{datetime.datetime.now()}] Realizando clusterização com o algoritmo KMeans...")

        # Determinar DataFrame base
        df = self._classificar_grupos_de_metricas(self._dados)

        # Criar o modelo KMeans
        kmeans = skl_cluster.KMeans(n_clusters=num_clusters, random_state=42)

        # Ajustar o modelo aos dados
        kmeans.fit(df)

        # Obter os rótulos dos clusters
        labels = kmeans.labels_

        # Adicionar os rótulos dos clusters ao DataFrame original
        df = self._classificar_grupos_de_metricas(df, reverter=True)
        df['Cluster'] = labels

        return df

    def _classificar_grupos_de_metricas(self, df: pd.DataFrame, reverter: bool = False) -> pd.DataFrame:
        # Criar DataFrames distintos para cada grupo de métrica
        if reverter:
            df_endividamento = df.loc[:, GrupoMetricasEnum.ENDIVIDAMENTO.value].div(self._PESO_ENDIVIDAMENTO)
            df_liquidez = df.loc[:, GrupoMetricasEnum.LIQUIDEZ.value].div(self._PESO_LIQUIDEZ)
            df_escala = df.loc[:, GrupoMetricasEnum.ESCALA.value].div(self._PESO_ESCALA)
        else:
            df_endividamento = df.loc[:, GrupoMetricasEnum.ENDIVIDAMENTO.value] * self._PESO_ENDIVIDAMENTO
            df_liquidez = df.loc[:, GrupoMetricasEnum.LIQUIDEZ.value] * self._PESO_LIQUIDEZ
            df_escala = df.loc[:, GrupoMetricasEnum.ESCALA.value] * self._PESO_ESCALA

        # Agrupar novamente os DataFrames
        return pd.concat([df_endividamento, df_liquidez, df_escala], axis=1)
