import abc

import pandas as pd


class DadosBase(abc.ABC):
    @property
    @abc.abstractmethod
    def df(self) -> pd.DataFrame:
        pass
