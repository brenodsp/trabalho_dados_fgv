import abc

import pandas as pd


class FinancialCollector(abc.ABC):
    @property
    @abc.abstractmethod
    def financial_infos(self) -> pd.DataFrame:
        pass