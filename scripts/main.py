from pathlib import Path

from backtester import backtest
from create_signal import create_signal
from preprocessing import preprocessing
from memory_reducer import memory_reducer


BASE_DIR = Path(__file__).resolve().parent.parent
stock_prices_path = BASE_DIR / "data" / "stock_prices.csv"
sp500_path = BASE_DIR / "data" / "sp500.csv"


def main():
    stock, sp500 = memory_reducer(stock_prices_path, sp500_path)
    stock, sp500 = preprocessing(stock, sp500)
    stock = create_signal(stock, sp500)
    backtest(stock, sp500)


if __name__ == "__main__":
    main()
