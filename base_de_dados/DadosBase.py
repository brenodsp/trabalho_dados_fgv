import abc
import os

import pandas as pd


class DadosBase(abc.ABC):
    _PASTA_BASE_DE_DADOS = "base_de_dados"
    _ARQUIVO_BASE_DE_DADOS = "base_de_dados.csv"
    
    @property
    def df(self) -> pd.DataFrame:
        path_base_dados = os.path.join(os.getcwd(), self._PASTA_BASE_DE_DADOS, self._ARQUIVO_BASE_DE_DADOS)
        if os.path.exists(path_base_dados):
            return self._ler_base_existente(path_base_dados)
        else:
            return self._construir_base_de_dados(path_base_dados)

    @staticmethod
    def _ler_base_existente(path: str) -> pd.DataFrame:
        return pd.read_csv(path)

    @abc.abstractmethod
    def _construir_base_de_dados(self, path_base_dados: str) -> pd.DataFrame:
        pass
