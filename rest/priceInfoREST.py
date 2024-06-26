import logging
from flask import Blueprint, jsonify
from dao.platformDAOFactory import DAOFactory
from dao.mt5CommonDAO import Mt5CommonDAO

# Set up the logger
logger = logging.getLogger('logger_info')

price_info_blueprint = Blueprint('price_info_blueprint', __name__)

@price_info_blueprint.route('/price/<string:symbol>', methods=['GET'])
def get_symbol_news(symbol: str, platform='mt5'):
    '''Get price info for a symbol'''
    logger.info('-----------------------------------------------------------------')
    logger.info(f"Received request for price info of symbol: {symbol} on platform: {platform}")
    logger.info('-----------------------------------------------------------------')
    
    try:
        price_info = Mt5CommonDAO.getCurrentPriceInfo(symbol)
        logger.info(f"Successfully retrieved price info for symbol: {symbol}, price: {price_info.to_dict()}")
        return jsonify(price_info.to_dict()), 200
    except Exception as e:
        logger.error(f"Error retrieving price info for symbol: {symbol} - {str(e)}")
        return jsonify({"error": str(e)}), 500
