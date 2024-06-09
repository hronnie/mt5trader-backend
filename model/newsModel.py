class News:
    def __init__(self, date: str, country: str, title: str, impact: str):
        self.date = date
        self.country = country
        self.title = title
        self.impact = impact

    def to_dict(self):
        return {
            'date': self.date,
            'country': self.country,
            'title': self.title,
            'impact': self.impact,
        }