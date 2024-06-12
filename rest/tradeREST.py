import re
from flask import Blueprint, request, jsonify
from dao.platformDAOFactory import DAOFactory
from service.tradeService import TradeService
from model.tradeResultModel import TradeResult
import datetime


trade_blueprint = Blueprint('trade_blueprint', __name__)


@trade_blueprint.route('/trade/long/<string:symbol>', methods=['POST'])
def trade_long(symbol: str, platform = 'mt5') -> TradeResult:
    '''Create long position'''
    params = request.get_json()
    slPrice = params.get('slPrice', '')
    tpPrice = params.get('tpPrice', '')
    entryPrice = params.get('entryPrice', '')
    trade_result = TradeService.createLongOrder(symbol, slPrice, tpPrice, entryPrice)
    return jsonify(trade_result.to_dict()), 200


@trade_blueprint.route('/trade/short/<string:symbol>', methods=['POST'])
def trade_short(symbol: str, platform = 'mt5') -> TradeResult:
    '''Create short position'''
    params = request.get_json()
    slPrice = params.get('slPrice', '')
    tpPrice = params.get('tpPrice', '')
    entryPrice = params.get('entryPrice', '')
    trade_result = TradeService.createShortOrder(symbol, slPrice, tpPrice, entryPrice)
    return jsonify(trade_result.to_dict()), 200

