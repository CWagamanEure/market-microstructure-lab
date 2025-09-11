import seaborn as sns
from typing import Literal
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal


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
        self.sell_bucket = defaultdict(float)
        self.buy_bucket = defaultdict(float)

    def __repr__(self):
        return (
            "LimitOrderBook(\n"
            f"  sell_limits={self.sell_limit_orders!r},\n"
            f"  buy_limits={self.buy_limit_orders!r},\n"
            f"  sell_markets={self.sell_market_orders!r},\n"
            f"  buy_markets={self.buy_market_orders!r}\n"
            ")"
        )

    def split_orders(self):
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

    def round_to_tick(price: float) -> Decimal:

        TICK = Decimal("0.01")
        d = Decimal(str(price))
        return (d / TICK).quantize(0) * TICK

    def merge_limits(self):
        for order in self.buy_limit_orders:
            key = order.price
            self.buy_bucket[key] += float(order.quantity)

        for order in self.sell_limit_orders:
            key = order.price
            self.sell_bucket[key] += float(order.quantity)

    def show_buckets(self):
        print("=== ORDER BUCKETS ===")
        print("-- BIDS (buy) --")
        for price, qty in sorted(
            self.buy_bucket.items(), key=lambda x: x[0], reverse=True
        ):
            print(f"  {price:>8.2f} : {qty:.2f}")

        print("-- ASKS (sell) --")
        for price, qty in sorted(self.sell_bucket.items(), key=lambda x: x[0]):
            print(f"  {price:>8.2f} : {qty:.2f}")

    def plot_auction_curves(self):
        bid_prices = sorted(self.buy_bucket.keys(), reverse=True)
        ask_prices = sorted(self.sell_bucket.keys())
        
        bid_qtys = [float(self.buy_bucket[p])  for p in bid_prices]
        ask_qtys = [float(self.sell_bucket[p]) for p in ask_prices]

        bid_cum = np.cumsum(bid_qtys)
        ask_cum = np.cumsum(ask_qtys)

        plt.step(bid_cum, bid_prices, where="post", label="Demand")
        plt.step(ask_cum, ask_prices, where="post", label="Supply")
        plt.xlabel("Cumulative Quantity")
        plt.ylabel("Price")
        plt.title("Supply & Demand from Buckets")
        plt.grid(True); plt.legend(); plt.tight_layout()
        plt.show()


def run(market_orders, limit_orders):
    book = LimitOrderBook(market_orders, limit_orders)
    book.split_orders()
    book.merge_limits()
    book.plot_auction_curves()

limit_orders = [
    LimitOrder("buy", 101, 5),
    LimitOrder("buy", 100, 3),
    LimitOrder("buy", 100, 4),
    LimitOrder("buy", 99,  6),
    LimitOrder("buy", 99,  2),
    LimitOrder("buy", 98,  7),
    LimitOrder("buy", 98,  1),
    LimitOrder("buy", 97,  8),
    LimitOrder("buy", 97,  3),
    LimitOrder("buy", 96,  9),
    LimitOrder("buy", 95,  5),
    LimitOrder("buy", 95,  2),
    LimitOrder("buy", 94,  4),
    LimitOrder("buy", 94,  6),
    LimitOrder("buy", 93,  3),

    LimitOrder("sell", 102, 4),
    LimitOrder("sell", 102, 2),
    LimitOrder("sell", 103, 6),
    LimitOrder("sell", 103, 3),
    LimitOrder("sell", 104, 5),
    LimitOrder("sell", 104, 1),
    LimitOrder("sell", 105, 7),
    LimitOrder("sell", 105, 2),
    LimitOrder("sell", 106, 8),
    LimitOrder("sell", 107, 6),
    LimitOrder("sell", 107, 4),
    LimitOrder("sell", 108, 3),
    LimitOrder("sell", 108, 5),
    LimitOrder("sell", 109, 2),
    LimitOrder("sell", 110, 9),
]

market_orders = [MarketOrder("buy", 5), MarketOrder("buy", 10), MarketOrder("sell", 4)]

run(market_orders, limit_orders)
