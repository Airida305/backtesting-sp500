import numpy as np
import pandas as pd


def preprocessing(stock_prices, sp500):
    stock_prices = stock_prices.copy()
    sp500 = sp500.copy()

    stock_prices["Date"] = pd.to_datetime(stock_prices["Date"])
    stock_prices = stock_prices.sort_values("Date")

    prices = stock_prices.set_index("Date").resample("M").last()
    prices = prices.apply(pd.to_numeric, errors="coerce")
    prices = prices.mask((prices < 0.1) | (prices > 10000))

    monthly_past_return = prices.div(prices.shift(1)).sub(1)
    monthly_future_return = prices.shift(-1).div(prices).sub(1)

    original_future_na_mask = monthly_future_return.isna()

    non_crisis_rows = ~monthly_past_return.index.year.isin([2008, 2009])
    non_crisis_mask = pd.DataFrame(
        np.repeat(non_crisis_rows[:, None], monthly_past_return.shape[1], axis=1),
        index=monthly_past_return.index,
        columns=monthly_past_return.columns,
    )

    past_outlier_mask = (
        (monthly_past_return > 1) | (monthly_past_return < -0.5)
    ) & non_crisis_mask
    future_outlier_mask = (
        (monthly_future_return > 1) | (monthly_future_return < -0.5)
    ) & non_crisis_mask

    monthly_past_return = monthly_past_return.mask(past_outlier_mask)
    monthly_future_return = monthly_future_return.mask(future_outlier_mask)

    prices = prices.ffill()
    monthly_past_return = monthly_past_return.ffill()
    monthly_future_return = monthly_future_return.ffill()
    monthly_future_return = monthly_future_return.mask(original_future_na_mask)

    prices_long = prices.stack(dropna=False).rename("Price")
    past_long = monthly_past_return.stack(dropna=False).rename("monthly_past_return")
    future_long = monthly_future_return.stack(dropna=False).rename(
        "monthly_future_return"
    )

    prices = pd.concat([prices_long, past_long, future_long], axis=1)
    prices.index.names = ["Date", "ticker"]
    prices = prices.sort_index().dropna()

    print(prices.isna().sum())

    sp500["Date"] = pd.to_datetime(sp500["Date"])
    sp500 = sp500.sort_values("Date")
    sp500 = sp500.set_index("Date").resample("M").last()
    sp500["monthly_past_return"] = sp500["Adjusted Close"].div(
        sp500["Adjusted Close"].shift(1)
    ).sub(1)
    sp500 = sp500[["Adjusted Close", "monthly_past_return"]].dropna()

    print("completed preprocessing")
    return prices, sp500