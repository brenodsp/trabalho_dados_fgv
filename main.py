from base_de_dados import DadosBaseYahoo
from clusterizacao import Clusterizador


# Declarar a base de dados utilizada
dados = DadosBaseYahoo().df

# Calcular clusters e expô-los em um DataFrame
num_clusters = 4
clusters = Clusterizador(dados).clusterizar(num_clusters)

a = 0
