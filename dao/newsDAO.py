import logging
from model.newsModel import News
import requests
from datetime import datetime, date
import pytz


logger = logging.getLogger('logger_info')

class NewsDAO:

    @staticmethod
    def fetch_json():
        """Fetch JSON data from a URL."""
        logger.info('Entered fetch_json')
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
            logger.info('Fetched JSON data successfully')
            return json_data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching JSON data: {e}")
            return []

    @staticmethod
    def filter_news_by_date_and_country(news_data, symbol):
        """Filter news items by today's date and country."""
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered filter_news_by_date_and_country')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: symbol={symbol}')

        today = date.today()
        filtered_news = []

        for item in news_data:
            news_date = datetime.fromisoformat(item['date']).date()
            if news_date == today and item['country'] == symbol:
                news = News(date=item['date'], country=item['country'], title=item['title'], impact=item['impact'])
                filtered_news.append(news)

        logger.info(f'Result: {filtered_news}')
        return filtered_news

    @classmethod
    def getAllNews(cls, symbolName) -> list[News]:
        logger.info('-----------------------------------------------------------------')
        logger.info('Entered getAllNews')
        logger.info('-----------------------------------------------------------------')
        logger.info(f'Input parameters: symbolName={symbolName}')
        
        news_data = cls.fetch_json()

        if symbolName != "ALL": 
            symbol1 = symbolName[:3]
            symbol2 = symbolName[3:]
            filtered_news_symbol1 = cls.filter_news_by_date_and_country(news_data, symbol1)
            filtered_news_symbol2 = cls.filter_news_by_date_and_country(news_data, symbol2)
            result = filtered_news_symbol1 + [news for news in filtered_news_symbol2 if news not in filtered_news_symbol1]
        else: 
            result = news_data
        

        logger.info(f'Result: {result}')
        return result
