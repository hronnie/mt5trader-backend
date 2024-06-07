from abc import ABC, abstractmethod
from model.priceInfoModel import PriceInfo

class BasePlatformDAO(ABC):

    @abstractmethod
    def getCurrentPriceInfo(self, symbolName) -> PriceInfo:
        pass
