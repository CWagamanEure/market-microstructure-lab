import seaborn as sns
from typing import Literal


class LimitOrder:
    def __init__(self, side: Literal["buy", "sell"], price: float, quantity: float):
        self.side = side
        self.price = price
        self.quantity = quantity


class MarketOrder:
    def __init__(self, side: Literal["buy", "sell"], quantity: float):
        self.side = side
        self.quantity = quantity


class LimitOrderBook:
    def __init__(
        self,
        market_order_list: list["MarketOrder"] | None = None,
        limit_order_list: list["LimitOrder"] | None = None,
    ):
        self.market_order_list: list[MarketOrder] = market_order_list or []
        self.limit_order_list: list[LimitOrder] = limit_order_list or []

    def sort_orders(self):
        market_order_list.sort(key=lambda o: o.price)
        limit_order_list.sort(key=lambda o: o.price)

    def match_orders(self):
        pass


limit_orders = [
    LimitOrder("buy", 101, 5),
    LimitOrder("buy", 3, 6),
    LimitOrder("sell", 20, 1),
]

market_orders = [MarketOrder("buy", 5), MarketOrder("buy", 10), MarketOrder("sell", 4)]

book = LimitOrderBook(market_orders, limit_orders)
book.sort_orders()
