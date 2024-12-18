import enum

class MetricasEnum(enum.Enum):
    DIVIDA_ATIVO = enum.auto()
    DIVIDA_RECEITA = enum.auto()
    DIVIDA_EBITDA = enum.auto()
    FLUXO_CAIXA_LIVRE = enum.auto()
    CAIXA = enum.auto()
    MARKET_CAP = enum.auto()

class GrupoMetricasEnum(enum.Enum):
    ENDIVIDAMENTO = [MetricasEnum.DIVIDA_ATIVO.name, MetricasEnum.DIVIDA_RECEITA.name, MetricasEnum.DIVIDA_EBITDA.name]
    LIQUIDEZ = [MetricasEnum.FLUXO_CAIXA_LIVRE.name, MetricasEnum.CAIXA.name]
    ESCALA = [MetricasEnum.MARKET_CAP.name]
