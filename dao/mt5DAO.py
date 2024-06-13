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
        spread_rounded = round(spread, 6)
        bid_rounded = round(symbol_info_tick_dict.bid, 5)
        ask_rounded = round(symbol_info_tick_dict.ask, 5)
        return PriceInfo(bid_rounded, ask_rounded, spread_rounded)

        

