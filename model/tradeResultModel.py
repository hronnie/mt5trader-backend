import datetime

class TradeResult:
    def __init__(self, executionDate: datetime.datetime, volume: float, entryPrice: float, comment: str, symbol: str,
                 slPrice: float, tpPrice: float, moneyAtRisk: float, tpPipValue: float, slPipValue: float, spread: float):
        self.executionDate = executionDate
        self.volume = volume
        self.entryPrice = entryPrice
        self.comment = comment
        self.symbol = symbol
        self.slPrice = slPrice
        self.tpPrice = tpPrice
        self.moneyAtRisk = moneyAtRisk
        self.tpPipValue = tpPipValue
        self.slPipValue = slPipValue
        self.spread = spread

    def to_dict(self):
        return {
            'executionDate': self.executionDate,
            'volume': self.volume,
            'entryPrice': self.entryPrice,
            'comment': self.comment,
            'symbol': self.symbol,
            'slPrice': self.slPrice,
            'tpPrice': self.tpPrice,
            'moneyAtRisk': self.moneyAtRisk,
            'tpPipValue': self.tpPipValue,
            'slPipValue': self.slPipValue,
            'spread': self.spread,
        }
