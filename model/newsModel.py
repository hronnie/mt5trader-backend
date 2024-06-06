from typing import Optional

class News:
    def __init__(self, date: str, impact: str, description: str):
        self.date = date
        self.impact = impact
        self.description = description

    def to_dict(self):
        return {
            'date': self.date,
            'impact': self.impact,
            'description': self.description,
        }