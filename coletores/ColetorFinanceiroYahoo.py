from .ColetorFinanceiro import ColetorFinanceiro

import pandas as pd
import yfinance as yf


class ColetorFinanceiroYahoo(ColetorFinanceiro):
    def __init__(self, ticker: str):
        super().__init__()
        self._ticker = ticker

    @property
    def _ticker_obj(self) -> yf.Ticker:
        return yf.Ticker(self._ticker)
    
    @property
    def NOME_EMPRESA(self) -> str:
        return self._ticker_obj.info['shortName']
    
    @property
    def _dados_financeiros_anualizados(self) -> pd.DataFrame:
        # Pegar informações básicas para o cálculo das métricas
        fluxo_caixa = self._fluxo_caixa_info['FreeCashFlow']
        ebitda = self._demonstrativo_financeiro_info['EBITDA']
        receita = self._demonstrativo_financeiro_info['TotalRevenue']
        ativos = self._balanco_financeiro_info['TotalAssets']
        passivos = self._balanco_financeiro_info['TotalLiabilitiesNetMinorityInterest']
        caixa = self._balanco_financeiro_info['CashAndCashEquivalents']
        num_acoes = self._ticker_obj.info['sharesOutstanding']
        preco_acao = self._pegar_preco_fechamento_anual(self._ticker_obj.history(period="5y", interval="1mo")['Close'])
        
        # Calcular métricas
        endividamento_ativos = self._calcular_endividamento_ativos(passivos, ativos)
        endividamento_receita = self._calcular_endividamento_receita(passivos, receita)
        fluxo_caixa_normalizado = self._calcular_fluxo_caixa_livre_normalizado(fluxo_caixa, ebitda)
        caixa_normalizado = self._calcular_caixa_normalizado(caixa, ebitda)
        market_cap = self._calcular_market_cap(preco_acao, num_acoes)

        return self._agregar_metricas_anualizadas(
            endividamento_ativos,
            endividamento_receita,
            fluxo_caixa_normalizado,
            caixa_normalizado,
            market_cap
        )
    
    @property
    def _fluxo_caixa_info(self) -> pd.DataFrame:
        df = self._ticker_obj.get_cashflow().T
        df.index = df.index.year
        
        return df.iloc[:4, :]
    
    @property
    def _demonstrativo_financeiro_info(self) -> pd.DataFrame:
        df = self._ticker_obj.get_financials().T
        df.index = df.index.year
        
        return df.iloc[:4, :]
    
    @property
    def _balanco_financeiro_info(self) -> pd.DataFrame:
        df = self._ticker_obj.get_balance_sheet().T
        df.index = df.index.year
        
        return df.iloc[:4, :]
    
    @staticmethod
    def _pegar_preco_fechamento_anual(serie_preco: pd.Series) -> pd.Series:
        """
        Pegar o preço de fechamento do ano para os anos anteriores, e o preço mais recente para o ano atual.

        TODO: A regra está generalista para todos os anos, inclusive o atual. Como estamos em dezembro, a regra funcionará,
        mas é recomendado parametrizar o ano mais recente de forma individualizada futuramente.
        """
        serie_preco_ajustada = serie_preco[serie_preco.index.month == 12]
        serie_preco_ajustada.index = serie_preco_ajustada.index.year

        return serie_preco_ajustada.sort_index(ascending=False).iloc[:4]
    
    @staticmethod
    def _agregar_metricas_anualizadas(
        endividamento_ativos: pd.Series,
        endividamento_receita: pd.Series,
        fluxo_caixa_normalizado: pd.Series,
        caixa_normalizado: pd.Series,
        market_cap: pd.Series
    ) -> pd.DataFrame:
        return pd.concat(
            [endividamento_ativos, endividamento_receita, fluxo_caixa_normalizado, caixa_normalizado, market_cap],
            axis=1
        )
