import numpy as np
import pandas as pd


def create_signal(stock_prices, sp500):
    stock_prices = stock_prices.copy()

    stock_prices = stock_prices.sort_index()
    stock_prices["average_return_1y"] = (
        stock_prices.groupby(level="ticker")["monthly_past_return"]
        .rolling(window=12, min_periods=12)
        .mean()
        .reset_index(level=0, drop=True)
    )

    ranks = stock_prices.groupby(level="Date")["average_return_1y"].rank(
        method="first", ascending=False
    )
    stock_prices["signal"] = ranks <= 20

    print("Signal creation completed")
    return stock_prices