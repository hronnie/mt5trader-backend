from model.tradeResultModel import TradeResult 
import datetime

class TradeService:

   
    @classmethod
    def createLongOrder(self, symbolName, slPrice, tpPrice, entryPrice) -> TradeResult:
        # TODO: implement real mt5 connector
        long_order = TradeResult(
            executionDate=datetime.datetime.now(),
            volume=1.1,  # 100k units (standard lot)
            entryPrice=1.2000,
            comment="Request executed",
            symbol="EURUSD",
            slPrice=1.1900,
            tpPrice=1.2100,
            moneyAtRisk=100,  
            tpPipValue=15,  
            slPipValue=3,  
            spread=0.00005
        )
        return long_order


    @classmethod
    def createShortOrder(self, symbolName, slPrice, tpPrice, entryPrice) -> TradeResult:
        # TODO: implement real mt5 connector
        short_order = TradeResult(
        executionDate=datetime.datetime.now(),
        volume=1.1,  
        entryPrice=1.2000,
        comment="Request executed",
        symbol="EURUSD",
        slPrice=1.2100,
        tpPrice=1.1900,
        moneyAtRisk=100, 
        tpPipValue=15,  
        slPipValue=3, 
        spread=0.00005
        )
        return short_order

