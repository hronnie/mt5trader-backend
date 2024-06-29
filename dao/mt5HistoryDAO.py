
import logging
import MetaTrader5 as mt5
from model.historyModel import TradeHistory
from datetime import datetime
from dao.mt5CommonDAO import Mt5CommonDAO


logger = logging.getLogger('logger_info')

class Mt5HistoryDAO:

    @classmethod
    def get_trading_history(cls) -> list[TradeHistory]:
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered get_trading_history')
        logger.info('-----------------------------------------------------------------')

        history_list = []
        mt5.initialize()
        from_date = datetime(2020, 1, 1)
        to_date = datetime.now()
        history = mt5.history_deals_get(from_date, to_date)
        history_orders = mt5.history_orders_get(from_date, to_date)

        if history is None:
            return history_list
        elif len(history) > 0:
            for history_item in history:
                sl, tp = Mt5CommonDAO.get_sl_tp_from_order(history_orders, history_item.position_id)
                if history_item.symbol is None or history_item.symbol == "": 
                    continue
                history_entry = TradeHistory(
                    ticket=history_item.ticket,
                    order=history_item.order,
                    time=history_item.time,
                    type=history_item.type,
                    entry=history_item.entry,
                    position_id=history_item.position_id,
                    reason=history_item.reason,
                    volume=history_item.volume,
                    price=history_item.price,
                    sl = sl,
                    tp = tp,
                    commission=history_item.commission,
                    swap=history_item.swap,
                    profit=history_item.profit,
                    fee=history_item.fee,
                    symbol=history_item.symbol,
                    comment=history_item.comment,
                    )
                history_list.append(history_entry)
                
            logger.info("result: ")
            for history_entry in history_list:
                logger.info(history_entry.to_dict())

            return history_list
