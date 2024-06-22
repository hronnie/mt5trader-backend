import re
from flask import Blueprint, jsonify
from dao.mt5DAO import Mt5DAO
from model.positionModel import TradePosition
from model.tradeResultModel import TradeResult
import logging

position_blueprint = Blueprint('position_blueprint', __name__)
logger = logging.getLogger('logger_info')

@position_blueprint.route('/position/all', methods=['GET'])
def get_all_position() -> list['TradePosition']:
    '''Get current active position for all symbol'''
    logger.info('-----------------------------------------------------------------')
    logger.info('Entered get_all_position')
    logger.info('-----------------------------------------------------------------')

    try:
        positions = Mt5DAO.get_positions()
        positions_list = [position_item.to_dict() for position_item in positions]
        logger.info(f'Result: {positions_list}')
        return jsonify(positions_list), 200
    except Exception as e:
        logger.error(f'Error in get_all_position: {str(e)}')
        return jsonify({"error": str(e)}), 500

@position_blueprint.route('/position/close/<int:ticket>', methods=['POST'])
def close_position(ticket: int) -> TradeResult:
    '''Close a position by its ticket number'''
    logger.info('-----------------------------------------------------------------')
    logger.info('Entered close_position')
    logger.info('-----------------------------------------------------------------')

    
    try:
        close_result = Mt5DAO.close_position_by_ticket(ticket)
        logger.info(f'Result: {close_result}')
        if close_result is None: 
            return jsonify({"Close was not successful"}), 500
        return jsonify(close_result.to_dict()), 200
    except Exception as e:
        logger.error(f'Error in close_position: {str(e)}')
        return jsonify({"error": str(e)}), 500
