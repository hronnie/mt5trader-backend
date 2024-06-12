import re
from flask import Blueprint, request, jsonify
from dao.platformDAOFactory import DAOFactory

price_info_blueprint = Blueprint('price_info_blueprint', __name__)


@price_info_blueprint.route('/price/<string:symbol>', methods=['GET'])
def get_symbol_news(symbol: str, platform = 'mt5'):
    '''Get price info for a symbol'''
    price_dao = DAOFactory.getDAO(platform)
    price_info = price_dao.getCurrentPriceInfo(symbol)
    return jsonify(price_info.to_dict()), 200

