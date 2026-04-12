from pathlib import Path
import numpy as np
import pandas as pd


def preprocessing(stock_prices, sp500):
    stock_prices = stock_prices.copy()
    sp500 = sp500.copy()

    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULTS_DIR = BASE_DIR / "results"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    stock_prices["Date"] = pd.to_datetime(stock_prices["Date"])
    stock_prices = stock_prices.sort_values("Date")

    raw_long = (
        stock_prices.melt(id_vars="Date", var_name="ticker", value_name="price")
        .sort_values(["ticker", "Date"])
        .reset_index(drop=True)
    )

    raw_long["daily_return"] = raw_long.groupby("ticker")["price"].pct_change(fill_method=None)

    price_outliers = raw_long[
        ((raw_long["price"] < 0.1) | (raw_long["price"] > 10000))
        & raw_long["price"].notna()
    ][["ticker", "Date", "price"]]

    return_outliers = raw_long[
        ((raw_long["daily_return"] > 1) | (raw_long["daily_return"] < -0.5))
        & (~raw_long["Date"].dt.year.isin([2008, 2009]))
        & raw_long["price"].notna()
    ][["ticker", "Date", "price"]]

    outliers = (
        pd.concat([price_outliers, return_outliers], axis=0)
        .drop_duplicates(subset=["ticker", "Date", "price"])
        .sort_values(["ticker", "Date"])
        .head(5)
        .copy()
    )

    outliers["Date"] = outliers["Date"].dt.strftime("%Y-%m-%d")

    with open(RESULTS_DIR / "outliers.txt", "w", encoding="utf-8") as file:
        for _, row in outliers.iterrows():
            file.write(f"{row['ticker']},{row['Date']},{row['price']}\n")

    prices = stock_prices.set_index("Date").resample("ME").last()
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

    prices_long = prices.stack().rename("Price")
    past_long = monthly_past_return.stack().rename("monthly_past_return")
    future_long = monthly_future_return.stack().rename("monthly_future_return")

    prices = pd.concat([prices_long, past_long, future_long], axis=1)
    prices.index.names = ["Date", "ticker"]
    prices = prices.sort_index().dropna()

    print(prices.isna().sum())

    sp500["Date"] = pd.to_datetime(sp500["Date"])
    sp500 = sp500.sort_values("Date")
    sp500 = sp500.set_index("Date").resample("ME").last()
    sp500["monthly_past_return"] = (
        sp500["Adjusted Close"].div(sp500["Adjusted Close"].shift(1)).sub(1)
    )
    sp500 = sp500[["Adjusted Close", "monthly_past_return"]].dropna()

    print("completed preprocessing")
    return prices, sp500