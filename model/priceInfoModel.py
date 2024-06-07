

class PriceInfo:
    def __init__(self, bidPrice: str, askPrice: str, spread: str):
        self.bidPrice = bidPrice
        self.askPrice = askPrice
        self.spread = spread

    def to_dict(self):
        return {
            'bidPrice': self.bidPrice,
            'askPrice': self.askPrice,
            'spread': self.spread,
        }