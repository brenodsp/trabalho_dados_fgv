from base_de_dados import DadosBaseYahoo
from clusterizacao import Clusterizador
from saidas.GeradorDeGraficos import GeradorDeGraficos

import os


# Declarar a base de dados utilizada
dados = DadosBaseYahoo().df

# Calcular clusters e expô-los em um DataFrame
num_clusters = 4
clusters = Clusterizador(dados.set_index('NOME_EMPRESA')).clusterizar(num_clusters)

# Determinar local de escrita das saídas
subpasta = 'saidas'
arquivo_csv = 'clusters.csv'
caminho_completo = os.path.join(subpasta, arquivo_csv)

# Criar a subpasta se ela não existir
os.makedirs(subpasta, exist_ok=True)

# Escrever o DataFrame em CSV na subpasta, sobrescrevendo o arquivo se ele já existir
clusters.reset_index().to_csv(caminho_completo, index=False)

# Apresentar gráficos
graficos = GeradorDeGraficos(clusters).gerar_graficos
