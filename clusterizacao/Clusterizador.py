from base_de_dados.DadosBase import DadosBase

import datetime

import pandas as pd
import sklearn.cluster as skl_cluster


class Clusterizador:
    def __init__(self, dados: DadosBase):
        self._dados = dados

    def clusterizar(self, num_clusters: int, estado_randomico: int = 42) -> pd.DataFrame:
        print(f"[{datetime.datetime.now()}] Realizando clusterização com o algoritmo KMeans...")

        # Determinar DataFrame base
        df = self._dados

        # Criar o modelo KMeans
        kmeans = skl_cluster.KMeans(n_clusters=num_clusters, random_state=42)

        # Ajustar o modelo aos dados
        kmeans.fit(df)

        # Obter os rótulos dos clusters
        labels = kmeans.labels_

        # Adicionar os rótulos dos clusters ao DataFrame original
        df['Cluster'] = labels

        return df
