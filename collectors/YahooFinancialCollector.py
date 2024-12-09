from .FinancialCollector import FinancialCollector

import pandas as pd
import yfinance as yf

class YahooFinancialCollector(FinancialCollector):
    def __init__(self, ticker: str):
        super().__init__()
        self._ticker = ticker

    @property
    def financial_infos(self) -> pd.DataFrame:
        dados = yf.Ticker(self._ticker).info
        return dados
