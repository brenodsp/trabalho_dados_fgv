from .DadosBase import DadosBase
from coletores import ColetorFinanceiroYahoo

import datetime
import os

import pandas as pd


class DadosBaseYahoo(DadosBase):
    """
    Todas as empresas do S&P500 (17/12/2024).

    Obs.: Exceto empresas sem EBITDA (BRK-B, JPN, BAC, WFC, MS, C, BK, GS) -> Instituições financeiras.
    Obs.: Empresas com menos de 5 anos de dados de preços (KVUE).
    """
    EMPRESAS = [
        "AAPL", "MSFT", "NVDA", "AMZN", "META", "TSLA", "AVGO", "GOOGL",
        "LLY", "V", "XOM", "UNH", "COST", "MA", "WMT", "HD", "PG", "NFLX", "JNJ",
        "CRM", "ABBV", "ORCL", "CVX", "MRK", "KO", "CSCO", "NOW", "ACN",
        "PEP", "MCD", "IBM", "LIN", "AMD", "ADBE", "DIS", "TMO", "ABT", "PM", "ISRG",
        "INTU", "CAT", "GE", "QCOM", "TXN", "BKNG", "VZ", "AXP", "T", "SPGI",
        "RTX", "HON", "PLTR", "DHR", "CMCSA", "NEE", "BLK", "LOW", "PGR", "AMGN", "PFE",
        "UNP", "ETN", "AMAT", "TJX", "BX", "BSX", "PANW", "COP", "SYK", "UBER",
        "BA", "ADP", "VRTX", "ANET", "MU", "FI", "SCHW", "GILD", "BMY", "TMUS", "DE",
        "ADI", "SBUX", "KKR", "MMC", "MDT", "LMT", "CB", "LRCX", "PLD", "UPS", "PYPL",
        "MO", "NKE", "EQIX", "APH", "AMT", "TT", "CRWD", "SO", "INTC", "ICE",
        "CMG", "KLAC", "PH", "ELV", "CDNS", "CME", "SHW", "DUK", "MDLZ", "USB", "SNPS",
        "PNC", "ZTS", "AON", "MSI", "WM", "REGN", "MCO", "CI", "CL", "CEG", "EMR", "WELL",
        "MCK", "ORLY", "ITW", "CTAS", "TDG", "MMM", "EOG", "COF", "GD", "APD", "MAR",
        "NOC", "WMB", "BDX", "ADSK", "FDX", "CSX", "ECL", "AJG", "HLT", "FTNT", "TGT",
        "TFC", "CARR", "OKE", "PCAR", "GM", "CVS", "FCX", "ROP", "ABNB", "RCL",
        "HCA", "AZO", "DLR", "SLB", "JCI", "TRV", "SRE", "SPG", "NXPI", "NSC", "AMP",
        "CPRT", "FICO", "AFL", "ALL", "KMI", "URI", "GWW", "PWR", "CMI", "ROST", "VST",
        "PSA", "AEP", "MET", "MSCI", "PSX", "O", "AXON", "AIG", "MPC", "HWM", "NEM",
        "TEL", "FIS", "PAYX", "D", "LULU", "FAST", "EW", "DFS", "KMB", "AME", "DHI",
        "PRU", "PEG", "PCG", "RSG", "LHX", "CCI", "CBRE", "BKR", "KR", "CTVA",
        "IR", "TRGP", "A", "COR", "VRSK", "VLO", "CTSH", "DAL", "F", "SYY", "IT", "OTIS",
        "YUM", "XEL", "EA", "HES", "ODFL", "KDP", "GLW", "MNST", "CHTR", "LEN", "GEHC",
        "VMC", "GIS", "STZ", "EXC", "WAB", "IDXX", "RMD", "DELL", "ACGL", "IQV", "EFX",
        "ROK", "HPQ", "MLM", "DD", "MTB", "NDAQ", "GRMN", "EXR", "IRM", "HIG", "AVB",
        "DECK", "ETR", "VICI", "WTW", "MCHP", "ED", "UAL", "OXY", "HUM", "EIX", "CNC",
        "EBAY", "FITB", "CSGP", "MPWR", "DXCM", "TTWO", "STT", "WEC", "ANSS", "TSCO",
        "KEYS", "FANG", "RJF", "NUE", "GDDY", "XYL", "GPN", "PPG", "ON", "CAH", "HPE",
        "DOW", "DOV", "KHC", "SYF", "BR", "SW", "FTV", "MTD", "EQT", "TROW", "HSY", "NVR",
        "TYL", "CCL", "NTAP", "CHD", "WBD", "VLTO", "AWK", "DTE", "HBAN", "EQR", "CPAY",
        "ADM", "BRO", "HAL", "VTR", "HUBB", "PHM", "PTC", "WST", "PPL", "CINF", "CDW",
        "AEE", "RF", "TPL", "SBAC", "EXPE", "TDY", "IFF", "WAT", "BIIB", "ATO", "ZBH",
        "K", "LYV", "WY", "WDC", "NTRS", "PKG", "TER", "ZBRA", "CNP", "STE", "ES", "LDOS",
        "CBOE", "CFG", "FE", "DVN", "FSLR", "CLX", "ULTA", "MKC", "STX", "CMS", "DRI",
        "LUV", "NRG", "LYB", "IP", "LH", "ESS", "INVH", "COO", "BLDR", "PODD", "SNA",
        "LVS", "EL", "MAA", "FDS", "CTRA", "TRMB", "WRB", "PNR", "OMC", "BALL", "STLD",
        "MOH", "BBY", "J", "TSN", "DGX", "IEX", "MAS", "KEY", "SMCI", "HOLX", "PFG",
        "EXPD", "DG", "GPC", "KIM", "VRSN", "NI", "ALGN", "GEN", "ARE", "DPZ", "CF",
        "AVY", "EG", "APTV", "LNT", "FFIV", "JBL", "L", "TXT", "BAX", "VTRS", "TPR",
        "AKAM", "DOC", "SWKS", "JBHT", "AMCR", "RVTY", "MRNA", "DLTR", "EVRG", "POOL",
        "EPAM", "ROL", "UDR", "KMX", "CAG", "HST", "JKHY", "CHRW", "CPT", "SWK", "JNPR",
        "REG", "DAY", "NDSN", "SJM", "TECH", "ALLE", "LW", "BXP", "NCLH", "ALB", "CTLT",
        "BG", "PAYC", "EMN", "AIZ", "IPG", "INCY", "UHS", "NWSA", "ERIE", "FOXA", "TAP",
        "GNRC", "CRL", "LKQ", "PNW", "ENPH", "GL", "SOLV", "HSIC", "HRL", "AES", "RL",
        "MKTX", "AOS", "FRT", "CPB", "WYNN", "TFX", "MTCH", "MOS", "MGM", "IVZ", "APA",
        "BF-B", "HAS", "CZR", "HII", "BWA", "CE", "WBA", "DVA", "BEN", "QRVO", "MHK",
        "PARA", "FMC", "FOX", "NWS", "AMTM"
    ]


    def __init__(self):
        super().__init__()


    def _construir_base_de_dados(self, path_base_dados: str) -> pd.DataFrame:        
        # Criar DataFrame da base de dados completa
        scores = []
        num_empresas = len(self.EMPRESAS)
        for n, ticker in enumerate(self.EMPRESAS):
            empresa = ColetorFinanceiroYahoo(ticker)
            print(f"[{datetime.datetime.now()}] Calculando score da empresa '{empresa.NOME_EMPRESA}' ({n+1}/{num_empresas})")

            try:
                score = ColetorFinanceiroYahoo(ticker).score_financeiro
                scores.append(score)
            except KeyError:
                print(f"[{datetime.datetime.now()}] EBITDA não encontrado (instituição financeira?)")
            except AttributeError:
                print(f"[{datetime.datetime.now()}] Histórico de preços muito pequeno")

        # Escrever base de dados em um arquivo CSV
        df = pd.concat(scores, axis=0)
        df.to_csv(path_base_dados, index=False)

        # Retornar base criada
        return df
