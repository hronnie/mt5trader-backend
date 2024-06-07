from model.priceInfoModel import PriceInfo

class Mt5DAO:

   
    @classmethod
    def getCurrentPriceInfo(self, symbolName) -> PriceInfo:
        # TODO: implement real mt5 connector
        return PriceInfo("1.08978", "1.25877", "0.00005")

