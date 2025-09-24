"""
Concentrated Liquidity Visuals
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt


class CLVizConfig:
    k = 10_000.0
    x_min = 50.0
    x_max = 200.0
    x0 = 100.0 #x reserves
    y0 = 100.0 #y reserves
    swap_in_x = 10.0 #deposited 10 units of x
    fee_bp = 30.0

    p_min = 2000
    p_max = 5000
    tight_lo = 3800
    tight_hi = 4200
    wide_level = 1.0
    tight_level = 8.0

    mu = 2000.0
    sigma = 150.0


    OUT = "./vis"


class ConcentratedLiquidity:
    def __init__(self, cfg):
        self.cfg = cfg
        os.makedirs(cfg.OUT, exist_ok=True)


    def plot_cpamm_curve(self, filename="cpamm_curve.png"):
        c = self.cfg
        x = np.linspace(c.x_min, c.x_max, 500)
        y = c.k / x

        fee_fraction = c.fee_bp / 10_000.0
        effective_in = c.swap_in_x * (1.0-fee_fraction)

        x1 = c.x0 + effective_in
        y1 = c.k / x1

        plt.figure()
        plt.plot(x, y, label="Invariant: x * y = k")
        plt.scatter([c.x0, x1], [c.y0, y1], s=50)
        plt.annotate(f"Start (x={c.x0:.2f}, y={c.y0:.2f})",
                     (c.x0, c.y0), xytext=(c.x0 + 8, c.y0 + 18),
                     arrowprops=dict(arrowstyle="->"))
        plt.annotate(f"After swap (x={x1:.2f}, y={y1:.2f})",
                     (x1, y1), xytext=(x1 - 35, y1 + 22),
                     arrowprops=dict(arrowstyle="->"))
        plt.title("CPAMM Invariant Curve and a Single Swap")
        plt.xlabel("Reserve X")
        plt.ylabel("Reserve Y")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        path = os.path.join(c.OUT, filename)
        plt.savefig(path, dpi=180)
        plt.close()
        return path

    def plot_liquidity_profiles(self, filename="liquidity_profiles.png"):
        c = self.cfg
        P = np.linspace(c.p_min, c.p_max, 1000)
        wide_liq = np.full_like(P, c.wide_level)

        tight_liq = np.zeros_like(P)
        mask = (P >= c.tight_lo) & (P <= c.tight_hi)
        tight_liq[mask] = c.tight_level

        plt.figure()
        plt.plot(P, wide_liq, drawstyle="steps-mid", label="Wide range (0 - ∞)")
        plt.plot(P, tight_liq, drawstyle="steps-mid",
                 label=f"Tight range ({int(c.tight_lo)} - {int(c.tight_hi)})")
        plt.title("Liquidity Density vs Price (Conceptual)")
        plt.xlabel("Price")
        plt.ylabel("Relative Liquidity Density")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        path = os.path.join(c.OUT, filename)
        plt.savefig(path, dpi=180)
        plt.close()
        return path


cfg = CLVizConfig()
cl = ConcentratedLiquidity(cfg)
cl.plot_cpamm_curve()
cl.plot_liquidity_profiles()
