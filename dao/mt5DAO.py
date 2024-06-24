import logging
from model.priceInfoModel import PriceInfo
import MetaTrader5 as mt5
from model.tradeResultModel import TradeResult
from model.positionModel import TradePosition
from datetime import datetime

logger = logging.getLogger('logger_info')

class Mt5DAO:

    @staticmethod
    def get_raw_spread(symbol_name): 
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered get_raw_spread')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: symbol_name={symbol_name}')
        symbol_info_tick_dict = mt5.symbol_info_tick(symbol_name)
        spread = abs(symbol_info_tick_dict.bid - symbol_info_tick_dict.ask)
        spread = round(spread, 5)
        logger.info(f'Spread result: {spread}')
        return spread

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
    def create_mt5_order(cls, lot_size, symbol, is_buy: bool, sl_price, ratio, entry_price_input=None, tp_price_input=None) -> TradeResult:
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered create_mt5_order')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: lot_size={lot_size}, symbol={symbol}, is_buy={is_buy}, sl_price={sl_price}, ratio={ratio}, entry_price_input={entry_price_input}, tp_price_input={tp_price_input}')
        
        mt5.initialize()

        point = mt5.symbol_info(symbol).point
        price_info = cls.getCurrentPriceInfo(symbol)
        entry_price = price_info.askPrice if is_buy else price_info.bidPrice
        spread_raw = cls.get_raw_spread(symbol)
        sl_price = sl_price - spread_raw if is_buy else sl_price + spread_raw

        action = mt5.SYMBOL_TRADE_EXECUTION_MARKET
        if entry_price_input is not None and entry_price_input != 0:
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

        if is_buy and entry_price_input is not None and entry_price_input != 0:
            if entry_price > price_info.bidPrice: 
                type = mt5.ORDER_TYPE_BUY_STOP_LIMIT
            else:     
                type = mt5.ORDER_TYPE_BUY_LIMIT
        if not is_buy and entry_price_input is not None and entry_price_input != 0: 
            if entry_price < price_info.askPrice: 
                type = mt5.ORDER_TYPE_SELL_STOP_LIMIT
            else:     
                type = mt5.ORDER_TYPE_SELL_LIMIT

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

        logger.info(f'Order request: {request}')

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
            spread=cls.get_pip_diff(symbol, result.ask, result.bid)
        )

        logger.info("Order creation result: %s", result)
        logger.info("TradeResult: %s", result_order)

        return result_order
    
    @classmethod
    def get_pip_diff(cls, symbol_name, entry, exit):
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
    
    @staticmethod
    def convert_time(mt5_time):
        return datetime.fromtimestamp(mt5_time).strftime('%Y.%m.%d %H:%M:%S')


    @classmethod
    def get_positions(cls) -> list['TradePosition']:
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered get_positions')
        logger.info('-----------------------------------------------------------------')
        positions_list = []
        mt5.initialize()
        positions = mt5.positions_get()

        if positions is None:
            return positions_list
        elif len(positions) > 0:
            for positionItem in positions:
                position = TradePosition(
                    symbol=positionItem.symbol,
                    ticket=positionItem.ticket,
                    time=cls.convert_time(positionItem.time),
                    type=positionItem.type,
                    volume=positionItem.volume,
                    price=positionItem.price_open,
                    sl=positionItem.sl,
                    tp=positionItem.tp,
                    current_price=positionItem.price_current,
                    profit=positionItem.profit
                )
                positions_list.append(position)
        
        return positions_list
                
    @classmethod
    def close_position_by_ticket(cls, ticket: int) -> TradeResult:
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered close_position_by_ticket')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: ticket={ticket}')
        
        mt5.initialize()
        
        # Retrieve the position to close
        positions = mt5.positions_get(ticket=ticket)
        
        if positions is None or len(positions) == 0:
            logger.info(f"No position found with ticket={ticket}, error code={mt5.last_error()}")
            return None
        
        position = positions[0]
        
        # Determine close order parameters
        symbol = position.symbol
        volume = position.volume
        order_type = mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).bid if position.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask
        
        # Prepare the close request
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": 234000,
            "comment": "Close position",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        logger.info(f'Close request: {request}')
        
        # Send the close request
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.info(f"Failed to close position, retcode={result.retcode}")
            return None
        
        # Create TradeResult for the closed position
        result_order = TradeResult(
            executionDate=datetime.now(),
            volume=volume,
            entryPrice=position.price_open,
            comment=result.comment,
            symbol=symbol,
            slPrice=position.sl,
            tpPrice=position.tp,
            moneyAtRisk=None,
            tpPipValue=None,
            slPipValue=None,
            spread=cls.get_pip_diff(symbol, result.price, position.price_open)
        )
        
        logger.info("Close position result: %s", result)
        logger.info("TradeResult: %s", result_order)
        
        return result_order    