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


class Auction:
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
        self.qnuma = 0
        self.qnumb = 0
        self.best_bid = 0
        self.best_ask = 0
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
    
    def calc_num_market_orders(self):
        self.qnumb= 0.0
        for order in self.buy_market_orders:
            self.qnumb += order.quantity            
        self.qnuma = 0.0
        for order in self.sell_market_orders:
            self.qnuma += order.quantity

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


    def find_best_bid_ask(self):
        ask_prices = self.sell_bucket.keys()
        bid_prices = self.buy_bucket.keys()
        self.best_bid = max(bid_prices)
        self.best_ask = min(ask_prices)
        print(f"Best Bid: {self.best_bid}")
        print(f"Best Ask: {self.best_ask}")

    def plot_auction_curves(self):
        bid_prices = sorted(self.buy_bucket.keys(), reverse=True)
        ask_prices = sorted(self.sell_bucket.keys())
        
        bid_qtys = [float(self.buy_bucket[p])  for p in bid_prices]
        ask_qtys = [float(self.sell_bucket[p]) for p in ask_prices]

        bid_cum = np.cumsum(bid_qtys) + float(self.qnumb)
        ask_cum = np.cumsum(ask_qtys) + float(self.qnuma)

        plt.step(bid_cum, bid_prices, where="post", label="Demand")
        plt.step(ask_cum, ask_prices, where="post", label="Supply")
        plt.xlabel("Cumulative Quantity")
        plt.ylabel("Price")
        plt.title("Supply & Demand from Buckets")
        plt.grid(True); plt.legend(); plt.tight_layout()
        plt.show()

        


def run(market_orders, limit_orders):
    auction = Auction(market_orders, limit_orders)
    auction.split_orders()
    auction.merge_limits()
    auction.calc_num_market_orders()
    auction.find_best_bid_ask()
    auction.plot_auction_curves()
    

limit_orders = [
    LimitOrder("buy", 3, 100),
    LimitOrder("buy", 4, 200),
    LimitOrder("buy", 3.50, 200),
    LimitOrder("buy", 2.50, 500),
    LimitOrder("sell", 5, 500),
    LimitOrder("sell", 3, 600),
    LimitOrder("sell", 4, 500),
]

market_orders = [MarketOrder("buy", 500), MarketOrder("sell", 200)]

run(market_orders, limit_orders)
