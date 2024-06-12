

class PriceInfo:
    def __init__(self, bidPrice: float, askPrice: float, spread: float):
        self.bidPrice = bidPrice
        self.askPrice = askPrice
        self.spread = spread

    def to_dict(self):
        return {
            'bidPrice': self.bidPrice,
            'askPrice': self.askPrice,
            'spread': self.spread,
        }