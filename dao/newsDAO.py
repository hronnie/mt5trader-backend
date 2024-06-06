from model.newsModel import News

class NewsDAO:

    def getAllNews(symbolName) -> list[News]:
        dummyNews = News(date="2024-06-06 12:10", impact="Hihg", description="Dummy news")
        return [dummyNews]
