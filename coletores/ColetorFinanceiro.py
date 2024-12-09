import abc

import pandas as pd


class ColetorFinanceiro(abc.ABC):
    @property
    @abc.abstractmethod
    def dados_financeiros(self) -> pd.DataFrame:
        """
        TODO: 
        - Calcular endividamento baseado nos ativos e na receita, fluxo de caixa livre (normalizar pelo EBITDA), 
        caixa (normalizado por EBITDA), MArket Cap.
        - Pegar métricas dos últimos 4 anos.
        - Pesar anos de forma decrescente (Peso 4 para última medição e 1 para a mais antiga) e fazer a média.
        """
        pass