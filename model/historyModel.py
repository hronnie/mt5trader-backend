from datetime import datetime


class TradeHistory:
    REASON_TYPES = {
        0: "Deal executed",
        1: "Stop-out",
        2: "Take Profit",
        3: "Stop Loss",
        4: "Deposition",
        5: "Withdrawal",
        6: "Interest rate",
        7: "Rebate",
        8: "Balance",
        9: "Credit",
        10: "Agent commission",
        11: "Swap",
        12: "Expired",
        13: "Manual",
        14: "Margin Call",
        15: "Closing position",
        16: "Modification",
        17: "Balance & credit",
        18: "Activation of bonus",
        19: "Cancelled dealer",
        20: "Withdrawn by the dealer",
        21: "Withdrawn by the administrator",
        22: "Delay order",
        23: "Cancelled client",
        24: "Cancelled dealer",
        25: "Rebate",
        26: "Cancelled order by dealer",
        27: "Cancelled order by client",
        28: "Exposure",
        29: "Cancelled withdrawal request",
        30: "Deleted bonus",
        31: "Correction",
        32: "Deleted API order",
        33: "Rebate",
        34: "Payment system",
        35: "Cancelled by payment system",
        36: "Broker to broker transfer",
        37: "Balance transfer",
        38: "Expired order",
        39: "Interest rate"
    }

    def __init__(self, ticket: int, order: int, time: int, type: int, entry: int, position_id: int, reason: int, volume: float, price: float, sl: float, tp: float, commission: float, swap: float, profit: float, fee: float, symbol: str, comment: str):
        self.ticket = ticket
        self.order = order
        self.time = time
        self.type = type
        self.entry = entry
        self.position_id = position_id
        self.reason = reason
        self.volume = volume
        self.price = price
        self.sl = sl
        self.tp = tp
        self.commission = commission
        self.swap = swap
        self.profit = profit
        self.fee = fee
        self.symbol = symbol
        self.comment = comment

    def to_dict(self):
        return {
            'ticket': self.ticket,
            'order': self.order,
            'time': self.time,
            'type': self.get_order_type(self.type),
            'position_id': self.position_id,
            'reason': self.get_reason_type(self.reason),
            'volume': self.volume,
            'entryPrice': self.price,
            'sl': self.sl,
            'tp': self.tp,
            'commission': self.commission,
            'swap': self.swap,
            'profit': self.profit,
            'fee': self.fee,
            'symbol': self.symbol,
            'comment': self.comment,
        }
    
    @staticmethod
    def get_order_type(order_type: int) -> str:
        if order_type == 0:
            return "Buy"
        elif order_type == 1:
            return "Sell"
        else:
            return "Unknown order type"

    @staticmethod
    def get_reason_type(reason_type: int) -> str:
        return TradeHistory.REASON_TYPES.get(reason_type, "Unknown reason type")
