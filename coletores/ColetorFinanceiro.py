from .enums import MetricasEnum

import abc

import pandas as pd


class ColetorFinanceiro(abc.ABC):
    NOME_EMPRESA: str

    @property
    @abc.abstractmethod
    def _dados_financeiros_anualizados(self) -> pd.DataFrame:
       pass

    @property
    def score_financeiro(self) -> pd.DataFrame:
        # Determinar peso de cada ano
        pesos = range(3, 0, -1)
        peso_total = sum([i for i in pesos])
        df = self._dados_financeiros_anualizados
        df['peso'] = pesos

        # Realizar média ponderada
        total_df = df.iloc[:, :-1].mul(df.iloc[:, -1], axis=0)
        total_df = total_df.sum() / peso_total

        # Ajustar formato do DataFrame
        df_final = total_df.to_frame().T
        df_final.index = [self.NOME_EMPRESA]

        return df_final

    def _calcular_endividamento_ativos(self, total_passivos: pd.Series, total_ativos: pd.Series) -> pd.Series:
        return self._atribuir_nome_serie(total_passivos.div(total_ativos), MetricasEnum.DIVIDA_ATIVO)
    
    def _calcular_endividamento_receita(self, total_passivos: pd.Series, receita: pd.Series) -> pd.Series:
        return self._atribuir_nome_serie(total_passivos.div(receita), MetricasEnum.DIVIDA_RECEITA)
    
    def _calcular_endividamento_ebitda(self, total_passivos: pd.Series, ebitda: pd.Series) -> pd.Series:
        return self._atribuir_nome_serie(total_passivos.div(ebitda), MetricasEnum.DIVIDA_EBITDA)
    
    def _calcular_fluxo_caixa_livre_normalizado(self, fluxo_caixa_livre: pd.Series, ebitda: pd.Series) -> pd.Series:
        return self._atribuir_nome_serie(fluxo_caixa_livre.div(ebitda), MetricasEnum.FLUXO_CAIXA_LIVRE)
    
    def _calcular_caixa_normalizado(self, caixa: pd.Series, ebitda: pd.Series) -> pd.Series:
        return self._atribuir_nome_serie(caixa.div(ebitda), MetricasEnum.CAIXA)
    
    def _calcular_market_cap(self, preco_acao: pd.Series, num_acoes: int) -> pd.Series:
        return self._atribuir_nome_serie(preco_acao * num_acoes, MetricasEnum.MARKET_CAP)
    
    @staticmethod
    def _atribuir_nome_serie(serie: pd.Series, enum_metrica: MetricasEnum) -> pd.Series:
        serie.name = enum_metrica.name
        return serie
