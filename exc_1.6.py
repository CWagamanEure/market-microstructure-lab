import seaborn as sns
from typing import Literal


class LimitOrder:
    def __init__(self, side: Literal["buy", "sell"], price: float, quantity: float):
        self.side = side
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return (
            f"LimitOrder(side={self.side!r}, price={self.price}, qty={self.quantity})"
        )


class MarketOrder:
    def __init__(self, side: Literal["buy", "sell"], quantity: float):
        self.side = side
        self.quantity = quantity

    def __repr__(self):
        return f"MarketOrder(side={self.side!r}, qty={self.quantity})"


class LimitOrderBook:
    def __init__(
        self,
        market_order_list: list["MarketOrder"] | None = None,
        limit_order_list: list["LimitOrder"] | None = None,
    ):
        self.market_order_list: list[MarketOrder] = market_order_list or []
        self.limit_order_list: list[LimitOrder] = limit_order_list or []
        self.sell_limit_orders = []
        self.buy_limit_orders = []
        self.sell_market_orders = []
        self.buy_market_orders = []

    def __repr__(self):
        return (
            "LimitOrderBook(\n"
            f"  sell_limits={self.sell_limit_orders!r},\n"
            f"  buy_limits={self.buy_limit_orders!r},\n"
            f"  sell_markets={self.sell_market_orders!r},\n"
            f"  buy_markets={self.buy_market_orders!r}\n"
            ")"
        )

    def split_and_sort_orders(self):
        for order in self.market_order_list:
            if order.side == "sell":
                self.sell_market_orders.append(order)
            else:
                self.buy_market_orders.append(order)
        for order in self.limit_order_list:
            if order.side == "sell":
                self.sell_limit_orders.append(order)
            else:
                self.buy_limit_orders.append(order)

        sort(self.mar)

    def match_orders(self):
        pass


limit_orders = [
    LimitOrder("buy", 101, 5),
    LimitOrder("buy", 3, 6),
    LimitOrder("sell", 20, 1),
]

market_orders = [MarketOrder("buy", 5), MarketOrder("buy", 10), MarketOrder("sell", 4)]

book = LimitOrderBook(market_orders, limit_orders)
print(book)
print()
book.split_and_sort_orders()

print(book)
