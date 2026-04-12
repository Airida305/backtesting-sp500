import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
import concurrent.futures
import os


def memory_reducer(stock_prices, sp500):
    stock_prices = pd.read_csv(stock_prices)
    sp500 = pd.read_csv(sp500)
    # Reduce memory usage by downcasting data types

    def reduce(df):
        for col in df.columns:
            if is_numeric_dtype(df[col]):
                min_val = df[col].min(skipna=True)
                max_val = df[col].max(skipna=True)

                if df[col].dtype.kind == "f":
                    df[col] = df[col].astype(np.float32)
                elif df[col].dtype.kind in ("u", "i"):
                    if (min_val >= np.iinfo(np.int8).min) and max_val <= np.iinfo(
                        np.int8
                    ).max:
                        df[col] = df[col].astype(np.uint8)
                    elif (min_val >= np.iinfo(np.int16).min) and max_val <= np.iinfo(
                        np.int16
                    ).max:
                        df[col] = df[col].astype(np.uint16)
                    elif (min_val >= np.iinfo(np.int32).min) and max_val <= np.iinfo(
                        np.int32
                    ).max:
                        df[col] = df[col].astype(np.uint32)
                    else:
                        df[col] = df[col].astype(np.uint64)
            else:
                if df[col].dtype == "object":
                    if "date" in col.lower():
                        df[col] = pd.to_datetime(df[col])
                    else:
                        df[col] = df[col].astype("category")
        return df

    stock_mem_before = stock_prices.memory_usage(deep=True).sum() / 1024**2
    sp500_mem_before = sp500.memory_usage(deep=True).sum() / 1024**2

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_stock = executor.submit(reduce, stock_prices)
        future_sp500 = executor.submit(reduce, sp500)
        stock_prices = future_stock.result()
        sp500 = future_sp500.result()

    stock_mem_after = stock_prices.memory_usage(deep=True).sum() / 1024**2
    sp500_mem_after = sp500.memory_usage(deep=True).sum() / 1024**2
    print(
        f"Memory usage: {stock_mem_before:.3f} MB -> {stock_mem_after:.3f} MB (stock_prices), "
        f"{sp500_mem_before:.3f} MB -> {sp500_mem_after:.3f} MB (sp500)"
    )
    print("Memory reduction completed")
    return stock_prices, sp500
