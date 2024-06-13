from model.priceInfoModel import PriceInfo
import MetaTrader5 as mt5

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
    def create_mt5_order(self, lot_size, symbol, is_buy: bool, sl_price, ratio, stop_limit_price = None, tp_price_input = None):
        mt5.initialize()

        point = mt5.symbol_info(symbol).point
        price_info = Mt5DAO.getCurrentPriceInfo(symbol)
        if is_buy: 
            entry_price = price_info.askPrice
        else: 
            entry_price = price_info.bidPrice

        action = mt5.SYMBOL_TRADE_EXECUTION_MARKET
        if stop_limit_price != None:
            entry_price = stop_limit_price
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

        if tp_price_input is not None: 
            tp_price = tp_price_input

        if is_buy and stop_limit_price != None:
            type = mt5.ORDER_TYPE_BUY_STOP_LIMIT
        if is_buy != True and stop_limit_price != None: 
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
        print(result)
        return result
    
    @classmethod
    def get_exit_price_pip(symbol_name, entry, exit):
        mt5.initialize()
        point = mt5.symbol_info(symbol_name).point
        diff = abs(exit - entry)
        return round(diff / point, 2)
