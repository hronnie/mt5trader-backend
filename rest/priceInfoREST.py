import logging
from flask import Blueprint, request, jsonify, current_app
import re
from dao.platformDAOFactory import DAOFactory

# Set up the logger
logger = logging.getLogger('price_info')

price_info_blueprint = Blueprint('price_info_blueprint', __name__)

@price_info_blueprint.route('/price/<string:symbol>', methods=['GET'])
def get_symbol_news(symbol: str, platform='mt5'):
    '''Get price info for a symbol'''
    logger.info(f"Received request for price info of symbol: {symbol} on platform: {platform}")
    
    try:
        price_dao = DAOFactory.getDAO(platform)
        price_info = price_dao.getCurrentPriceInfo(symbol)
        logger.info(f"Successfully retrieved price info for symbol: {symbol}, price: {price_info.to_dict()}")
        return jsonify(price_info.to_dict()), 200
    except Exception as e:
        logger.error(f"Error retrieving price info for symbol: {symbol} - {str(e)}")
        return jsonify({"error": str(e)}), 500
