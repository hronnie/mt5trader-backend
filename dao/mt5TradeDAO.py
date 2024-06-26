import logging
import MetaTrader5 as mt5
from model.tradeResultModel import TradeResult
from datetime import datetime
from dao.mt5CommonDAO import Mt5CommonDAO

logger = logging.getLogger('logger_info')

class Mt5TradeDAO:
    @classmethod
    def create_mt5_order(cls, lot_size, symbol, is_buy: bool, sl_price, ratio, entry_price_input=None, tp_price_input=None) -> TradeResult:
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered create_mt5_order')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: lot_size={lot_size}, symbol={symbol}, is_buy={is_buy}, sl_price={sl_price}, ratio={ratio}, entry_price_input={entry_price_input}, tp_price_input={tp_price_input}')
        
        mt5.initialize()

        point = mt5.symbol_info(symbol).point
        price_info = Mt5CommonDAO.getCurrentPriceInfo(symbol)
        entry_price = price_info.askPrice if is_buy else price_info.bidPrice
        spread_raw = Mt5CommonDAO.get_raw_spread(symbol)
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


        result = Mt5CommonDAO.order_send_to_mt5(action, symbol, lot_size, type, entry_price, sl_price, tp_price, "NORMAL")
        result_order = TradeResult(
            executionDate=datetime.now(),
            volume=lot_size,  
            entryPrice=entry_price,
            comment=result.comment,
            symbol=symbol,
            slPrice=sl_price,
            tpPrice=tp_price,
            moneyAtRisk=None, 
            tpPipValue=None,  
            slPipValue=None, 
            spread=Mt5CommonDAO.get_pip_diff(symbol, result.ask, result.bid)
        )

        logger.info("Order creation result: %s", result)
        logger.info("TradeResult: %s", result_order)

        return result_order