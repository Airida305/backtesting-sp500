# imports

from backtester import backtest
from create_signal import create_signal
from preprocessing import preprocessing
from memory_reducer import memory_reducer

stock_prices_path = "./data/stock_prices.csv"
sp500_path = "./data/sp500.csv"

# memory reducer
stock, sp500 = memory_reducer(stock_prices_path, sp500_path)
# preprocessing
preprocessing(stock, sp500)
# create signal

# backtest
