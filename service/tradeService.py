import logging
from model.tradeResultModel import TradeResult
import datetime
from dao.mt5DAO import Mt5DAO

logger = logging.getLogger('trade_service')

class TradeService:

    @classmethod
    def createOrder(cls, symbolName, slPrice, tpPrice, entryPrice, ratio, risk, is_long) -> TradeResult:
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered createLongOrder')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: symbolName={symbolName}, slPrice={slPrice}, tpPrice={tpPrice}, entryPrice={entryPrice}, ratio={ratio}, risk={risk}')
        
        volume, change_per_pip, money_at_risk = cls.calculate_lot_size(
            risk_percentage=risk, 
            stop_loss=slPrice, 
            symbol=symbolName, 
            is_buy_input=True
        )
        
        logger.info(f'Volume {volume}, Change per pip: {change_per_pip}, Money at risk: {money_at_risk}')
        
        order_result = Mt5DAO.create_mt5_order(volume, symbolName, is_long, slPrice, ratio, entryPrice, tpPrice)
        logger.info(f'Order result: {order_result}')
        
        tp_pip = Mt5DAO.get_pip_diff(symbolName, order_result.entryPrice, order_result.tpPrice)
        sl_pip = Mt5DAO.get_pip_diff(symbolName, order_result.entryPrice, order_result.slPrice)

        order_result.tpPipValue = tp_pip
        order_result.slPipValue = sl_pip
        order_result.moneyAtRisk = money_at_risk      

        logger.info(f'Result: {order_result.to_dict()}')
        
        return order_result        

    
    @classmethod
    def calculate_lot_size(cls, risk_percentage, stop_loss, symbol, is_buy_input):
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered calculate_lot_size')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: risk_percentage={risk_percentage}, stop_loss={stop_loss}, symbol={symbol}, is_buy_input={is_buy_input}')
        
        account_balance = Mt5DAO.getAccountBalance()
        logger.info(f'Account balance: {account_balance}')
        
        contract_size = 0
        if symbol == "XAUUSD":
            pip_size = 0.01
            contract_size = 100  
        else:
            pip_size = 0.01 if "JPY" in symbol else 0.0001
            contract_size = 100000  
        
        price_info = Mt5DAO.getCurrentPriceInfo(symbol)
        logger.info(f'Price info: {price_info}')
        
        eur_conv_price = None
        if is_buy_input:
            eur_conv_price = price_info.bidPrice
        else: 
            eur_conv_price = price_info.askPrice

        risk_amount = account_balance * (risk_percentage / 100)
        if symbol == "XAUUSD":
            pip_value = pip_size * contract_size
        else:
            pip_value = pip_size / eur_conv_price * contract_size

        stop_loss_pips = abs(eur_conv_price - stop_loss) / pip_size
        lot_size = risk_amount / (stop_loss_pips * pip_value)
        money_at_risk = stop_loss_pips * pip_value * lot_size
        change_per_pip = round(money_at_risk / stop_loss_pips, 2)

        result = round(lot_size, 2), change_per_pip, money_at_risk
        logger.info(f'Result: {result}')
        
        return result
