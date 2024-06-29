import logging
from model.priceInfoModel import PriceInfo
import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd

logger = logging.getLogger('logger_info')

class Mt5CommonDAO:

    @staticmethod
    def get_raw_spread(symbol): 
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered get_raw_spread')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: symbol_name={symbol}')

        symbol_info_tick_dict = mt5.symbol_info_tick(symbol)
        spread = abs(symbol_info_tick_dict.bid - symbol_info_tick_dict.ask)
        spread = round(spread, 5)
        logger.info(f'Spread result: {spread}')
        return spread
    
    @classmethod
    def get_pip_diff(cls, symbol_name, entry, exit):
        """
        Gets the number of pips between 2 prices
        """
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered get_pip_diff')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: symbol_name={symbol_name}, entry={entry}, exit={exit}')
        
        mt5.initialize()
        point = mt5.symbol_info(symbol_name).point * 10
        
        diff = abs(exit - entry)
        result = round(diff / point, 2)

        logger.info(f'point: {point}, diff: {diff}, result: {result}')
        return result

    @classmethod
    def getCurrentPriceInfo(cls, symbol_name) -> PriceInfo:
        """
        Fetches the current price of the given symbol.
        
        :param symbol: The ticker symbol of the asset to fetch the current price for.
        :return: The current price of the asset, or None if not found.
        """
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered getCurrentPriceInfo')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: symbol_name={symbol_name}')
        
        mt5.initialize()
        mt5.symbol_select(symbol_name, True)

        symbol_info_tick_dict = mt5.symbol_info_tick(symbol_name)
        spread = cls.get_raw_spread(symbol_name)
        point = mt5.symbol_info(symbol_name).point * 10
        spread = spread / point 
        spread_rounded = round(spread, 2)
        bid_rounded = round(symbol_info_tick_dict.bid, 5)
        ask_rounded = round(symbol_info_tick_dict.ask, 5)
        price_info = PriceInfo(bid_rounded, ask_rounded, spread_rounded)

        logger.info(f'Price info result: {price_info.to_dict()}')
        return price_info

    @classmethod
    def getAccountBalance(cls) -> float:
        """
        Gets current account balance
        """
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered getAccountBalance')
        logger.info('-----------------------------------------------------------------')
        
        mt5.initialize()
        account = mt5.account_info()
        balance = account.balance

        logger.info(f'Result: {balance}')
        return balance 
    
    
    @classmethod
    def order_send_to_mt5(cls, action, symbol, lot_size, order_type, entry_price, sl_price, tp_price, comment):
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered order_send_to_mt5')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: action={action}, symbol={symbol}, lot_size={lot_size}, sl_price={sl_price}, entry_price={entry_price}, order_type={order_type}, tp_price={tp_price}, comment={comment}')
        
        mt5.initialize()
        request = {
            "action": action,
            "symbol": symbol,
            "volume": lot_size,
            "type": order_type,
            "price": entry_price,
            "stoplimit": entry_price,
            "sl": sl_price,
            "tp": tp_price,
            "deviation": 20,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        logger.info(f'Order request: {request}')

        result = mt5.order_send(request)
        return result

    
    @staticmethod
    def convert_time(mt5_time):
        return datetime.fromtimestamp(mt5_time).strftime('%Y.%m.%d %H:%M:%S')
    
    @staticmethod
    def get_atr(symbol):
        logger.info('Calculating ATR...')
        logger.info(f'Input parameters: symbol={symbol}')

        atr_period = 14
        period = 100 
        timeframe=mt5.TIMEFRAME_M1
        
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, period + atr_period)
        df = pd.DataFrame(rates)
        df['tr1'] = df['high'] - df['low']
        df['tr2'] = (df['high'] - df['close'].shift(1)).abs()
        df['tr3'] = (df['low'] - df['close'].shift(1)).abs()
        df['tr'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
        df['atr'] = df['tr'].rolling(window=atr_period).mean()
        atr_value = df['atr'].iloc[-1]
        
        logger.info(f'ATR value calculated: {atr_value}')
        return atr_value

    @classmethod
    def calculate_new_sl_tp(cls, position): 
        position_dict = position.to_dict()
        
        atr_value = cls.get_atr(position.symbol)
        atr_multiplier = 3  

        pip_size = 0.0001 if 'JPY' not in position.symbol else 0.01
        atr_pips = atr_value / pip_size


        sl_diff_position = abs(position.entry_price - position.sl)
        new_sl_position = position.current_price - sl_diff_position if "Sell" in position_dict['type'] else position.current_price + sl_diff_position
        new_tp_position = position.sl

        sl_diff_atr = atr_pips * atr_multiplier * pip_size
        new_sl_atr = position.current_price - sl_diff_atr if "Sell" in position_dict['type'] else position.current_price + sl_diff_atr
        new_tp_atr = position.current_price + sl_diff_atr * 3 if "Sell" in position_dict['type'] else position.current_price - sl_diff_atr * 3

        logger.info(f"SL/TP values: sl_diff_position: {sl_diff_position}, new_sl_position: {new_sl_position}, new_tp_position: {new_tp_position}")
        logger.info(f"ATR values: sl_diff_atr: {sl_diff_atr}, new_sl_atr: {new_sl_atr}, new_tp_atr: {new_tp_atr}")


        if sl_diff_position < sl_diff_atr: 
            new_sl = new_sl_atr
            new_tp = new_tp_atr
        else: 
            new_sl = new_sl_position
            new_tp = new_tp_position    
        
        return new_sl, new_tp



    @classmethod
    def get_sl_tp_from_order(cls, history_orders, ticket):
        if history_orders is None:
            return None, None
        
        for item in history_orders:
            if ticket == item.ticket:
                return item.sl, item.tp
        
        # If ticket is not found in history_orders
        return None, None
    

