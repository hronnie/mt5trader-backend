from typing import Optional



class News:
    def __init__(self, time: str, currency: str, description: str):
        self.time = time
        self.currency = currency
        self.description = description

    def to_dict(self):
        return {
            'time': self.time,
            'currency': self.currency,
            'description': self.description,
        }