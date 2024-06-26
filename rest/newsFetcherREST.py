from flask import Blueprint, jsonify
from dao.newsDAO import NewsDAO
import logging

news_fetcher_blueprint = Blueprint('news_fetcher_blueprint', __name__)
news_dao = NewsDAO
logger = logging.getLogger('logger_info')

@news_fetcher_blueprint.route('/symbol-news/<string:symbol>', methods=['GET'])
def get_symbol_news(symbol: str):
    '''Get news for a symbol for today'''
    logger.info('-----------------------------------------------------------------')
    logger.info('Entered get_symbol_news')
    logger.info('-----------------------------------------------------------------')
    logger.info(f'Input parameters: symbol={symbol}')

    try:
        news = news_dao.getAllNews(symbol)
        news_list = [news_item.to_dict() for news_item in news]
        logger.info(f'Result: {news_list}')
        return jsonify(news_list), 200
    except Exception as e:
        logger.error(f'Error in get_symbol_news: {str(e)}')
        return jsonify({"error": str(e)}), 500
