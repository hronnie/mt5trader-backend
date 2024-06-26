import logging
import MetaTrader5 as mt5
from model.tradeResultModel import TradeResult
from model.positionModel import TradePosition
from datetime import datetime
from dao.mt5CommonDAO import Mt5CommonDAO

logger = logging.getLogger('logger_info')

class Mt5PositionDAO:
    @classmethod
    def create_hedge_position(cls, ticket):
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered create_hedge_position')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: ticket={ticket}')
        
        mt5.initialize()    
        position = cls.get_position_by_ticket(ticket)
        position_dict = position.to_dict()
        type = mt5.ORDER_TYPE_SELL if "Buy" in position_dict['type'] else mt5.ORDER_TYPE_BUY
        action = mt5.SYMBOL_TRADE_EXECUTION_MARKET

        sl_diff = abs(position.price - position.sl)
        new_sl = position.current_price - sl_diff if "Sell" in position_dict['type'] else position.current_price + sl_diff
        new_tp = position.sl

        logger.info(f"Creating hedge position with the following parameters: action={action}, symbol={position.symbol}, type={type}, entry_price={position.current_price},sl={new_sl}, tp={new_tp} ")

        result = Mt5CommonDAO.order_send_to_mt5(action, position.symbol, position.volume, type, position.current_price, new_sl, new_tp, "HEDGE")

        result_order = TradeResult(
            executionDate=datetime.now(),
            volume=position.volume,  
            entryPrice=position.current_price,
            comment=result.comment,
            symbol=position.symbol,
            slPrice=new_sl,
            tpPrice=new_tp,
            moneyAtRisk=None, 
            tpPipValue=None,  
            slPipValue=None, 
            spread=Mt5CommonDAO.get_pip_diff(position.symbol, result.ask, result.bid)
        )

        logger.info("Hedge Order creation result: %s", result)
        logger.info("Hedge TradeResult: %s", result_order)

        return result_order      
    
    @classmethod
    def flip_position_side(cls, ticket):
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered flip_position_side')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: ticket={ticket}')
        
        mt5.initialize()    
        position = cls.get_position_by_ticket(ticket)
        position_dict = position.to_dict()
        type = mt5.ORDER_TYPE_SELL if "Buy" in position_dict['type'] else mt5.ORDER_TYPE_BUY
        action = mt5.SYMBOL_TRADE_EXECUTION_MARKET
        
        # cancel original position
        close_position_result = cls.close_position_by_ticket(ticket)
        if close_position_result.comment != "Request executed": 
            return None

        # create new flipped position
        sl_diff = abs(position.price - position.sl)
        tp_diff = sl_diff * 3
        new_sl = position.current_price - sl_diff if "Sell" in position_dict['type'] else position.current_price + sl_diff
        new_tp = position.current_price + tp_diff if "Sell" in position_dict['type'] else position.current_price - tp_diff

        result = Mt5CommonDAO.order_send_to_mt5(action, position.symbol, position.volume, type, position.current_price, new_sl, new_tp, "FLIP")
        result_order = TradeResult(
            executionDate=datetime.now(),
            volume=position.volume,  
            entryPrice=position.current_price,
            comment=result.comment,
            symbol=position.symbol,
            slPrice=new_sl,
            tpPrice=new_tp,
            moneyAtRisk=None, 
            tpPipValue=None,  
            slPipValue=None, 
            spread=Mt5CommonDAO.get_pip_diff(position.symbol, result.ask, result.bid)
        )

        logger.info("Flip Order creation result: %s", result)
        logger.info("Flip TradeResult: %s", result_order)

        return result_order   

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
                    time=Mt5CommonDAO.convert_time(positionItem.time),
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
        
        positions = mt5.positions_get(ticket=ticket)
        
        if positions is None or len(positions) == 0:
            logger.info(f"No position found with ticket={ticket}, error code={mt5.last_error()}")
            return None
        
        position = positions[0]
        
        symbol = position.symbol
        volume = position.volume
        order_type = mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).bid if position.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask
        
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
        
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.info(f"Failed to close position, retcode={result.retcode}")
            return None
        
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
            spread=Mt5CommonDAO.get_pip_diff(symbol, result.price, position.price_open)
        )
        
        logger.info("Close position result: %s", result)
        logger.info("TradeResult: %s", result_order)
        
        return result_order    
    
    @classmethod
    def close_all_position(cls):
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered close_all_position')
        logger.info('-----------------------------------------------------------------')
        
        mt5.initialize()
        
        positions = cls.get_positions()
        for position in positions:
            cls.close_position_by_ticket(position.ticket)    
        
        return "Success"
    
    @classmethod
    def modify_position_by_ticket(cls, ticket: int, sl: float, tp: float) -> TradeResult:
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered modify_position_by_ticket')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: ticket={ticket}, sl={sl}, tp={tp}')
        
        mt5.initialize()
        
        positions = mt5.positions_get(ticket=ticket)
        
        if positions is None or len(positions) == 0:
            logger.info(f"No position found with ticket={ticket}, error code={mt5.last_error()}")
            return None
        
        position = positions[0]
        if sl is None or sl == 0: 
            sl = position.sl
        if tp is None or tp == 0: 
            tp = position.tp
        
        # Prepare the modification request
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": position.symbol,
            "position": ticket,
            "sl": sl,
            "tp": tp,
        }
        
        logger.info(f'Modify request: {request}')
        
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.info(f"Failed to modify position, retcode={result.retcode}")
            return None
        
        result_order = TradeResult(
            executionDate=datetime.now(),
            volume=position.volume,
            entryPrice=position.price_open,
            comment=result.comment,
            symbol=position.symbol,
            slPrice=sl,
            tpPrice=tp,
            moneyAtRisk=None,
            tpPipValue=None,
            slPipValue=None,
            spread=None
        )
        
        logger.info("Modify position result: %s", result)
        logger.info("TradeResult: %s", result_order)
        
        return result_order
    
    @classmethod
    def get_position_by_ticket(cls, ticket) -> TradePosition:
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered get_position_by_ticket')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: ticket={ticket}')
        positions = cls.get_positions()
        for position in positions:
            if position.ticket == ticket:
                return position
        return None