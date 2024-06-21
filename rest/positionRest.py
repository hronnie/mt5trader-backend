import re
from flask import Blueprint, jsonify
from dao.mt5DAO import Mt5DAO
from model.positionModel import TradePosition
import logging

position_blueprint = Blueprint('position_blueprint', __name__)
logger = logging.getLogger('logger_info')

@position_blueprint.route('/position/all', methods=['GET'])
def get_all_position() -> list['TradePosition']:
    '''Get current active position for all symbol'''
    logger.info('-----------------------------------------------------------------')
    logger.info('get_all_position get_symbol_news')
    logger.info('-----------------------------------------------------------------')

    try:
        positions = Mt5DAO.get_positions()
        positions_list = [position_item.to_dict() for position_item in positions]
        logger.info(f'Result: {positions_list}')
        return jsonify(positions_list), 200
    except Exception as e:
        logger.error(f'Error in get_symbol_news: {str(e)}')
        return jsonify({"error": str(e)}), 500
