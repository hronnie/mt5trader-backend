from flask import Blueprint, jsonify, request
from dao.mt5PositionDAO import Mt5PositionDAO
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
        positions = Mt5PositionDAO.get_positions()
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
    logger.info(f'Input: ticket: {ticket}')

    
    try:
        close_result = Mt5PositionDAO.close_position_by_ticket(ticket)
        logger.info(f'Result: {close_result.to_dict()}')
        if close_result is None: 
            return jsonify({"Close was not successful"}), 500
        return jsonify(close_result.to_dict()), 200
    except Exception as e:
        logger.error(f'Error in close_position: {str(e)}')
        return jsonify({"error": str(e)}), 500


@position_blueprint.route('/position/modify/<int:ticket>', methods=['POST'])
def modify_exit_orders(ticket: int) -> TradeResult:
    '''Modifies SL and/or TP'''
    logger.info('-----------------------------------------------------------------')
    logger.info('Entered modify_exit_orders')
    logger.info('-----------------------------------------------------------------')
    
    params = request.get_json()
    logger.info(f'Input parameters: ticket={ticket}, params={params}')
    
    sl = params.get('sl', '')
    tp = params.get('tp', '')
    try:
        modify_result = Mt5PositionDAO.modify_position_by_ticket(ticket, sl, tp)
        logger.info(f'Result: {modify_result.to_dict()}')
        if modify_result is None: 
            return jsonify({"Modify exit orders was not successful"}), 500
        return jsonify(modify_result.to_dict()), 200
    except Exception as e:
        logger.error(f'Error in modify_exit_orders: {str(e)}')
        return jsonify({"error": str(e)}), 500 
    

@position_blueprint.route('/position/breakeven/<int:ticket>', methods=['POST'])
def breakeven_position(ticket: int) -> TradeResult:
    '''Breakeven position'''
    logger.info('-----------------------------------------------------------------')
    logger.info('Entered breakeven_position')
    logger.info('-----------------------------------------------------------------')
    
    logger.info(f'Input parameters: ticket={ticket}')
    

    try:
        position = Mt5PositionDAO.get_position_by_ticket(ticket)
        if position is None: 
            return jsonify({"Couldn't find the position": str(e)}), 404 

        modify_result = Mt5PositionDAO.modify_position_by_ticket(ticket, position.price, position.tp)
        logger.info(f'Result: {modify_result.to_dict()}')
        if modify_result is None: 
            return jsonify({"Modify exit orders was not successful"}), 500
        return jsonify(modify_result.to_dict()), 200
    except Exception as e:
        logger.error(f'Error in modify_exit_orders: {str(e)}')
        return jsonify({"error": str(e)}), 500 
    

@position_blueprint.route('/position/hedge/<int:ticket>', methods=['POST'])
def hedge_position(ticket: int) -> TradeResult:
    '''Hedge position'''
    logger.info('-----------------------------------------------------------------')
    logger.info('Entered hedge_position')
    logger.info('-----------------------------------------------------------------')
    
    logger.info(f'Input parameters: ticket={ticket}')
    
    try:
        position = Mt5PositionDAO.get_position_by_ticket(ticket)
        if position is None: 
            return jsonify({"Couldn't find the position": str(e)}), 404 

        hedge_result = Mt5PositionDAO.create_hedge_position(ticket)
        logger.info(f'Result: {hedge_result.to_dict()}')
        if hedge_result is None: 
            return jsonify({"Creating hedge position was not successful"}), 500
        return jsonify(hedge_result.to_dict()), 200
    except Exception as e:
        logger.error(f'Error in hedge_position: {str(e)}')
        return jsonify({"error": str(e)}), 500 
    

@position_blueprint.route('/position/flip/<int:ticket>', methods=['POST'])
def flip_position(ticket: int) -> TradeResult:
    '''Flip position side'''
    logger.info('-----------------------------------------------------------------')
    logger.info('Entered flip_position')
    logger.info('-----------------------------------------------------------------')
    
    logger.info(f'Input parameters: ticket={ticket}')
    

    try:
        position = Mt5PositionDAO.get_position_by_ticket(ticket)
        if position is None: 
            return jsonify({"Couldn't find the position": str(e)}), 404 

        flip_result = Mt5PositionDAO.flip_position_side(ticket)
        logger.info(f'Result: {flip_result.to_dict()}')
        if flip_result is None: 
            return jsonify({"Modify exit orders was not successful"}), 500
        return jsonify(flip_result.to_dict()), 200
    except Exception as e:
        logger.error(f'Error in flip_position: {str(e)}')
        return jsonify({"error": str(e)}), 500 
    
@position_blueprint.route('/position/closeall', methods=['POST'])
def close_all_position() -> TradeResult:
    '''Closes all position'''
    logger.info('-----------------------------------------------------------------')
    logger.info('Entered close_all_position')
    logger.info('-----------------------------------------------------------------')  

    try:
        Mt5PositionDAO.close_all_position()
        return jsonify({"comment": "success"}), 200
    except Exception as e:
        logger.error(f'Error in close_all_position: {str(e)}')
        return jsonify({"comment": str(e)}), 500 