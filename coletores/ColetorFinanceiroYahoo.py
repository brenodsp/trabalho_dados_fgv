from .ColetorFinanceiro import ColetorFinanceiro

import pandas as pd
import yfinance as yf

class ColetorFinanceiroYahoo(ColetorFinanceiro):
    def __init__(self, ticker: str):
        super().__init__()
        self._ticker = ticker

    @property
    def dados_financeiros(self) -> pd.DataFrame:
        dados = yf.Ticker(self._ticker)
        return dados
