from model.priceInfoModel import PriceInfo
import MetaTrader5 as mt5
from model.tradeResultModel import TradeResult
import datetime


class Mt5DAO:

   
    @classmethod
    def getCurrentPriceInfo(self, symbol_name) -> PriceInfo:
        """
        Fetches the current price of the given symbol.
        
        :param symbol: The ticker symbol of the asset to fetch the current price for.
        :param is_long
        :return: The current price of the asset, or None if not found.
        """
        mt5.initialize()
        mt5.symbol_select(symbol_name, True)
        symbol_info_tick_dict = mt5.symbol_info_tick(symbol_name)
        spread = abs(symbol_info_tick_dict.bid - symbol_info_tick_dict.ask)
        point = mt5.symbol_info(symbol_name).point * 10
        spread = spread / point 
        spread_rounded = round(spread, 2)
        bid_rounded = round(symbol_info_tick_dict.bid, 5)
        ask_rounded = round(symbol_info_tick_dict.ask, 5)
        return PriceInfo(bid_rounded, ask_rounded, spread_rounded)

    @classmethod
    def getAccountBalance(self) -> float:
        """
        Gets current account balance
        """
        mt5.initialize()
        account = mt5.account_info()
        return account.balance
    
    @classmethod
    def create_mt5_order(self, lot_size, symbol, is_buy: bool, sl_price, ratio, entry_price_input = None, tp_price_input = None) -> TradeResult:
        mt5.initialize()

        point = mt5.symbol_info(symbol).point
        price_info = Mt5DAO.getCurrentPriceInfo(symbol)
        if is_buy: 
            entry_price = price_info.askPrice
        else: 
            entry_price = price_info.bidPrice

        action = mt5.SYMBOL_TRADE_EXECUTION_MARKET
        if entry_price_input != None and entry_price_input != 0:
            entry_price = entry_price_input
            action = mt5.TRADE_ACTION_PENDING
        
        one_pip = 10 * point
        sl_pips = abs(sl_price - entry_price) / one_pip
        sl_pips = round(sl_pips, 2)

        tp_price = None
        type = None
        if is_buy:
            type = mt5.ORDER_TYPE_BUY
            tp_price = entry_price + sl_pips * one_pip * ratio
        else: 
            type = mt5.ORDER_TYPE_SELL
            tp_price = entry_price - sl_pips * one_pip * ratio

        if tp_price_input is not None and tp_price_input != 0: 
            tp_price = tp_price_input

        if is_buy and entry_price_input != None and entry_price_input != 0:
            type = mt5.ORDER_TYPE_BUY_STOP_LIMIT
        if is_buy != True and entry_price_input != None and entry_price_input != 0: 
            type = mt5.ORDER_TYPE_SELL_STOP_LIMIT
        

        deviation = 20

        request = {
            "action": action,
            "symbol": symbol,
            "volume": lot_size,
            "type": type,
            "price": entry_price,
            "stoplimit": entry_price,
            "sl": sl_price,
            "tp": tp_price,
            "deviation": deviation,
            "comment": "hronnie python entry",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }



        result = mt5.order_send(request)
        result_order = TradeResult(
            executionDate=datetime.datetime.now(),
            volume=lot_size,  
            entryPrice=entry_price,
            comment=result.comment,
            symbol=symbol,
            slPrice=sl_price,
            tpPrice=tp_price,
            moneyAtRisk=None, 
            tpPipValue=None,  
            slPipValue=None, 
            spread=abs(result.ask - result.bid)
            )
        print("order creation result")
        print(result)
        print("TradeResult:")
        print(result_order)
        print('-------end ----')
        return result_order
    
    @classmethod
    def get_exit_price_pip(self, symbol_name, entry, exit):
        mt5.initialize()
        point = mt5.symbol_info(symbol_name).point * 10
        
        diff = abs(exit - entry)
        print(f"point: {point}, diff: {abs(exit - entry)}, result: {round(diff / point, 2)}")
        return round(diff / point, 2)
