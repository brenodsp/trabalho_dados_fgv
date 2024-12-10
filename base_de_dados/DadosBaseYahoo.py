from .DadosBase import DadosBase
from coletores import ColetorFinanceiroYahoo

import pandas as pd


class DadosBaseYahoo(DadosBase):
    """
    Empresas: Apple, Microsoft, Hershey's, Gamestop, Walmart, Boeing, Coca Cola, Cameco, Pfizer, Ralph Lauren, GM.
    """
    EMPRESAS = [
        'AAPL',
        'MSFT',
        'HSY',
        'GME',
        'WMT',
        'BA',
        'KO',
        'CCJ',
        'PFE',
        'RL',
        'GM'
    ]

    def __init__(self):
        super().__init__()

    @property
    def df(self) -> pd.DataFrame:
        scores = []
        for ticker in self.EMPRESAS:
            empresa = ColetorFinanceiroYahoo(ticker)
            print(f"Calculando score da empresa '{empresa.NOME_EMPRESA}'")

            score = ColetorFinanceiroYahoo(ticker).score_financeiro
            scores.append(score)

        return pd.concat(scores, axis=0)
