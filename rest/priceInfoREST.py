import re
from flask import Blueprint, request, jsonify
from dao.mt5DAO import Mt5DAO


price_info_blueprint = Blueprint('price_info_blueprint', __name__)
price_dao = Mt5DAO

@price_info_blueprint.route('/price/<string:symbol>', methods=['GET'])
def get_symbol_news(symbol: str):
    '''Get price info for a symbol'''
    price_info = price_dao.getCurrentPriceInfo(symbol)
    return jsonify(price_info.to_dict()), 200

