import matplotlib.axes
import matplotlib.axis
import matplotlib.collections
import matplotlib.colorbar
import matplotlib.figure
from coletores.enums import MetricasEnum

import os
import typing

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


class GeradorDeGraficos:
    _PATH_SAIDAS = "saidas"
    _MARCADOR_MAP = {0: 'o', 1: '*', 2: '^', 3: 's'}
    _TAMANHO_MAP = {0: 100, 1: 300, 2: 100, 3: 100}
    _LEGENDA_MAP = { 0: 'Cluster 0 (Círculo)', 1: 'Cluster 1 (Estrela)', 2: 'Cluster 2 (Triângulo)', 3: 'Cluster 3 (Quadrado)' }

    def __init__(self, saida_clusterizada: pd.DataFrame):
        self._df_grafico = self._preparar_df_para_graficos(saida_clusterizada)

    def _preparar_df_para_graficos(self, saida_clusterizada: pd.DataFrame) -> pd.DataFrame:
        # Adicionar guias para os marcadores
        saida_clusterizada['Marcador'] = saida_clusterizada['Cluster'].map(self._MARCADOR_MAP)
        saida_clusterizada['Tamanho'] = saida_clusterizada['Cluster'].map(self._TAMANHO_MAP)
        saida_clusterizada['Legenda'] = saida_clusterizada['Cluster'].map(self._LEGENDA_MAP)
        return saida_clusterizada
    
    def _criar_scatter_plot(
        self,
        ax: matplotlib.axes._axes.Axes,
        coluna_eixo_x: str,
        coluna_eixo_y: str,
        coluna_cores: str
    ) -> typing.Tuple[matplotlib.axes._axes.Axes, matplotlib.collections.PathCollection]:
        
        # Preencher dados
        scatter = []
        legendas = []
        for idx, row in self._df_grafico.iterrows():
            sc = ax.scatter(
                row[coluna_eixo_x], 
                row[coluna_eixo_y],
                c=row[coluna_cores], 
                vmin=self._df_grafico[coluna_cores].min(), 
                vmax=self._df_grafico[coluna_cores].max(), 
                marker=row['Marcador'], 
                s=row['Tamanho'], 
                cmap='viridis', 
                edgecolors='w', 
                label=row['Legenda'] if row['Cluster'] not in scatter else ""
            )
            scatter.append(row['Cluster'])

            if row['Legenda'] not in legendas: 
                legendas.append(row['Legenda'])
            # ax.text(row['DIVIDA_ATIVO'], row['DIVIDA_RECEITA'], row['NOME_EMPRESA'], fontsize=5, ha='right')

        # Adicionar a legenda 
        handles, labels = ax.get_legend_handles_labels() 
        by_label = dict(zip(labels, handles)) 
        ax.legend(by_label.values(), by_label.keys())

        # Definir rótulos e título
        ax.set_xlabel(coluna_eixo_x)
        ax.set_ylabel(coluna_eixo_y)

        return ax, sc

    @staticmethod
    def _adicionar_escala_de_cor(scatter_plot: matplotlib.collections.PathCollection, nome: str) -> matplotlib.colorbar.Colorbar:
        cbar = plt.colorbar(scatter_plot)
        cbar.set_label(nome)
        return cbar
    
    def _definir_titulo_e_salvar(self, axes: matplotlib.axes._axes.Axes, titulo: str) -> matplotlib.axes._axes.Axes:
        axes.set_title(titulo)
        plt.savefig(os.path.join(self._PATH_SAIDAS, titulo))
        return axes
    
    @property
    def analise_pela_divida(self) -> matplotlib.figure.Figure:
        # Criar gráfico
        fig, ax = plt.subplots()

        # Criar modelo de scatter plot
        ax, sc = self._criar_scatter_plot(
            ax, 
            MetricasEnum.DIVIDA_ATIVO.name,
            MetricasEnum.DIVIDA_RECEITA.name,
            MetricasEnum.DIVIDA_EBITDA.name
        )
        
        # Adicionar cor baseada na DIVIDA_EBITDA
        cbar = self._adicionar_escala_de_cor(sc, MetricasEnum.DIVIDA_EBITDA.name)

        # Adicionar título
        ax = self._definir_titulo_e_salvar(
            ax, 
            f'Relação entre {MetricasEnum.DIVIDA_ATIVO.name}, {MetricasEnum.DIVIDA_RECEITA.name} e {MetricasEnum.DIVIDA_EBITDA.name}'
        )
        
        return fig

    @property
    def analise_pelo_caixa(self) -> matplotlib.figure.Figure:
        # Criar gráfico
        fig, ax = plt.subplots()

        # Criar modelo de scatter plot
        ax, sc = self._criar_scatter_plot(
            ax, 
            MetricasEnum.FLUXO_CAIXA_LIVRE.name,
            MetricasEnum.CAIXA.name,
            'Cluster'
        )

        # Adicionar título
        ax = self._definir_titulo_e_salvar(
            ax,
            f'Relação entre {MetricasEnum.FLUXO_CAIXA_LIVRE.name} e {MetricasEnum.CAIXA.name}'
        )

        return fig
        
    @property
    def analise_pelo_market_cap(self) -> matplotlib.figure.Figure:
        # Criar gráfico
        fig, ax = plt.subplots()

        # Criar modelo de scatter plot
        ax, sc = self._criar_scatter_plot(
            ax, 
            'Cluster',
            MetricasEnum.MARKET_CAP.name,
            'Cluster'
        )

        # Adicionar título
        ax = self._definir_titulo_e_salvar(
            ax, 
            f'Relação entre {MetricasEnum.MARKET_CAP.name} e a formação dos clusters'
        )
        
        return fig

    @property
    def gerar_graficos(self) -> typing.Tuple[matplotlib.figure.Figure, matplotlib.figure.Figure, matplotlib.figure.Figure]:
        g1 = self.analise_pela_divida
        g2 = self.analise_pelo_caixa
        g3 = self.analise_pelo_market_cap

        plt.show()

        return g1, g2, g3