
class TradePosition:
    ORDER_TYPES = {
        0: "Market Buy",
        1: "Market Sell",
        2: "Buy Limit",
        3: "Sell Limit",
        4: "Buy Stop",
        5: "Sell Stop",
        6: "Buy Stop",
        7: "Sell Stop",
    }

    def __init__(self, symbol: str, ticket: int, time: str, type: int, volume: float, price: float, sl: float, tp: float, current_price: float, profit: float):
        self.symbol = symbol
        self.ticket = ticket
        self.time = time
        self.type = type
        self.volume = volume
        self.price = price
        self.sl = sl
        self.tp = tp
        self.current_price = current_price
        self.profit = profit

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'ticket': self.ticket,
            'time': self.time,
            'type': self.get_order_type(self.type),
            'volume': self.volume,
            'price': self.price,
            'sl': self.sl,
            'tp': self.tp,
            'current_price': self.current_price,
            'profit': self.profit,
        }
    
    @staticmethod
    def get_order_type(order_type: int) -> str:
        return TradePosition.ORDER_TYPES.get(order_type, "Unknown order type")
