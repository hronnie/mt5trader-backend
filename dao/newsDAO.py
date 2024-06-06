from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional
from model.newsModel import News
import random

class NewsDAO:

    @staticmethod
    def create_driver():
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        ]
        user_agent = random.choice(user_agent_list)

        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={user_agent}")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    @staticmethod
    def parse_data(driver, url):
        driver.get(url)
        # Get the table
        table = driver.find_element(By.CLASS_NAME, "calendar__table")
        news_list = []

        # Iterate over each table row
        for row in table.find_elements(By.TAG_NAME, "tr"):
            # list comprehension to get each cell's data and filter out empty cells
            row_data = list(filter(None, [td.text for td in row.find_elements(By.TAG_NAME, "td")]))
            if not row_data or len(row_data) < 3:
                continue
            
            time = row_data[0]
            currency = row_data[1]
            description = row_data[2]
            news = News(time=f'{time}', currency=f'{currency}', description=f'{description}')
            news_list.append(news)
        return news_list

    @staticmethod
    def filter_news(news_list, symbols):
        # Split the symbols string into individual currency codes
        symbol1 = symbols[:3]
        symbol2 = symbols[3:]

        # Filter news_list for each symbol individually
        filtered_news_symbol1 = [news for news in news_list if symbol1 in news.currency]
        filtered_news_symbol2 = [news for news in news_list if symbol2 in news.currency]

        # Combine the filtered results
        filtered_news = filtered_news_symbol1 + [news for news in filtered_news_symbol2 if news not in filtered_news_symbol1]
        
        return filtered_news

    @classmethod
    def getAllNews(cls, symbolName) -> list[News]:
        driver = cls.create_driver()
        url = 'https://www.forexfactory.com'

        news_list = cls.parse_data(driver=driver, url=url)
        filtered_news = cls.filter_news(news_list, symbolName)

        for news in filtered_news:
            print(news.to_dict())

        driver.quit()
        return filtered_news

