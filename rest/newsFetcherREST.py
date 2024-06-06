import re
from flask import Blueprint, request, jsonify
from dao.newsDAO import NewsDAO


news_fetcher_blueprint = Blueprint('news_fetcher_blueprint', __name__)
news_dao = NewsDAO

@news_fetcher_blueprint.route('/symbol-news/<string:symbol>', methods=['GET'])
def get_symbol_news(symbol: str):
    '''Get news for a symbol for today'''
    news = news_dao.getAllNews(symbol)
    news = [news_item.to_dict() for news_item in news]
    return jsonify(news), 200

