from flask import Blueprint, jsonify, request
from dao.mt5HistoryDAO import Mt5HistoryDAO
from model.positionModel import TradePosition
from model.tradeResultModel import TradeResult
import logging

history_blueprint = Blueprint('history_blueprint', __name__)
logger = logging.getLogger('logger_info')

@history_blueprint.route('/history/all', methods=['GET'])
def get_all_history() -> list['TradePosition']:
    '''Get all history items'''
    logger.info('-----------------------------------------------------------------')
    logger.info('Entered get_all_history')
    logger.info('-----------------------------------------------------------------')

    try:
        histories = Mt5HistoryDAO.get_trading_history()
        history_list = [history_item.to_dict() for history_item in histories]
        logger.info(f'Result: {history_list}')
        return jsonify(history_list), 200
    except Exception as e:
        logger.error(f'Error in get_all_history: {str(e)}')
        return jsonify({"error": str(e)}), 500