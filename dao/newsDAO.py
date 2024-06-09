from model.newsModel import News
import requests
from datetime import datetime, date
import pytz
class NewsDAO:

    @staticmethod
    def fetch_json():
        """Fetch JSON data from a URL."""
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching JSON data: {e}")
            return []

    @staticmethod
    def filter_news_by_date_and_country(news_data, symbol):
        """Filter news items by today's date and country."""
        today = date.today()
        filtered_news = []

        for item in news_data:
            news_date = datetime.fromisoformat(item['date']).date()
            if news_date == today and item['country'] == symbol:
                news = News(date=item['date'], country=item['country'], title=item['title'], impact=item['impact'])
                filtered_news.append(news)

        return filtered_news
    

    @classmethod
    def getAllNews(cls, symbolName) -> list[News]:
        news_data = cls.fetch_json()
        symbol1 = symbolName[:3]
        symbol2 = symbolName[3:]
        filtered_news_symbol1 = cls.filter_news_by_date_and_country(news_data, symbol1)
        filtered_news_symbol2 = cls.filter_news_by_date_and_country(news_data, symbol2)
        filtered_news = filtered_news_symbol1 + [news for news in filtered_news_symbol2 if news not in filtered_news_symbol1]

        for news in filtered_news:
            print(news.to_dict())

        return filtered_news

