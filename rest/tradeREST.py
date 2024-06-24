import re
from flask import Blueprint, request, jsonify, current_app
from dao.mt5DAO import Mt5DAO
from service.tradeService import TradeService
from model.tradeResultModel import TradeResult
import logging

trade_blueprint = Blueprint('trade_blueprint', __name__)
logger = logging.getLogger('logger_info')


def trade(symbol: str, params, is_long: str) -> TradeResult:
    '''Create position'''
    logger.info('-----------------------------------------------------------------')
    logger.info('Entered trade')
    logger.info('-----------------------------------------------------------------')
    params = request.get_json()
    logger.info(f'Input parameters: symbol={symbol}, params={params}')
    
    slPrice = params.get('slPrice', '')
    tpPrice = params.get('tpPrice', '')
    entryPrice = params.get('entryPrice', '')
    ratio = params.get('ratio', '')
    spread = params.get('spread', '')
    risk = params.get('risk', )
    
    try:
        price_info = Mt5DAO.getCurrentPriceInfo(symbol)
        if price_info.spread > spread: 
            trade_result = TradeResult(
                executionDate=None,
                volume=None,
                entryPrice=None,
                comment='Spread violation',
                symbol=None,
                slPrice=None,
                tpPrice=None,
                moneyAtRisk=None,
                tpPipValue=None,
                slPipValue=None,
                spread=price_info.spread
            )
        else: 
            trade_result = TradeService.createOrder(symbol, slPrice, tpPrice, entryPrice, ratio, risk, is_long)
        
        logger.info(f'Result: {trade_result.to_dict()}')
        return jsonify(trade_result.to_dict()), 200
    except Exception as e:
        logger.error(f'Error in trade_long: {str(e)}')
        return jsonify({"error": str(e)}), 500

@trade_blueprint.route('/trade/long/<string:symbol>', methods=['POST'])
def trade_long(symbol: str, platform='mt5') -> TradeResult:
    '''Create long position'''
    logger.info('-----------------------------------------------------------------')
    logger.info('Entered trade_long')
    logger.info('-----------------------------------------------------------------')
    params = request.get_json()
    logger.info(f'Input parameters: symbol={symbol}, params={params}')
    return trade(symbol, params, True)

@trade_blueprint.route('/trade/short/<string:symbol>', methods=['POST'])
def trade_short(symbol: str, platform='mt5') -> TradeResult:
    '''Create short position'''
    logger.info('-----------------------------------------------------------------')
    logger.info('Entered trade_short')
    logger.info('-----------------------------------------------------------------')
    params = request.get_json()
    logger.info(f'Input parameters: symbol={symbol}, params={params}')
    
    return trade(symbol, params, False)