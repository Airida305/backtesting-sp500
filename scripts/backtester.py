from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def backtest(stock_prices, sp500):
    stock_prices = stock_prices.copy()
    sp500 = sp500.copy()

    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULTS_DIR = BASE_DIR / "results"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # TASK. Is the PnL computed by multiplying the signal Series by the future returns?
    signal_series = stock_prices["signal"].astype(int)
    stock_prices["PnL"] = signal_series * stock_prices["monthly_future_return"]

    strategy_pnl = stock_prices.groupby(level="Date")["PnL"].sum().sort_index()

    total_strategy_pnl = stock_prices["PnL"].sum()
    # TASK. Is the return of the strategy computed by dividing the PnL by the sum of the signal Series?
    total_strategy_return = (
        total_strategy_pnl / signal_series.sum() if signal_series.sum() != 0 else np.nan
    )
    # TASK lower than 75.
    assert (
        total_strategy_pnl < 75
    ), "Total strategy PnL is unexpected result. must be < 75"
    sp500 = sp500.sort_index()

    # SP500 benchmark: 20$ each month
    sp500_signal = pd.Series(20, index=sp500.index, dtype=np.int64)
    sp500["PnL"] = sp500_signal * sp500["monthly_past_return"]

    benchmark_pnl = sp500["PnL"].sort_index()
    total_benchmark_pnl = benchmark_pnl.sum()
    total_benchmark_return = (
        total_benchmark_pnl / sp500_signal.sum() if sp500_signal.sum() != 0 else np.nan
    )

    # TASK Are the series used in the plot the cumulative PnL? cumsum can be used.
    common_index = strategy_pnl.index.intersection(benchmark_pnl.index)
    strategy_cum_pnl = strategy_pnl.loc[common_index].cumsum()
    benchmark_cum_pnl = benchmark_pnl.loc[common_index].cumsum()

    with open(RESULTS_DIR / "results.txt", "w", encoding="utf-8") as file:
        file.write("Stock Picking 20 Strategy\n")
        file.write(f"Total PnL: {total_strategy_pnl:.6f}\n")
        file.write(f"Total return: {total_strategy_return:.6f}\n\n")
        file.write("SP500 Benchmark Strategy\n")
        file.write(f"Total PnL: {total_benchmark_pnl:.6f}\n")
        file.write(f"Total return: {total_benchmark_return:.6f}\n")

    plt.figure(figsize=(12, 6))
    plt.plot(strategy_cum_pnl.index, strategy_cum_pnl.values, label="Stock Picking 20")
    plt.plot(benchmark_cum_pnl.index, benchmark_cum_pnl.values, label="SP500")
    plt.title("Cumulative PnL: Stock Picking 20 vs SP500")
    plt.xlabel("Date")
    plt.ylabel("Cumulative PnL")
    plt.xlim(strategy_cum_pnl.index.min(), strategy_cum_pnl.index.max())
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "plots/strategy_vs_sp500.png")
    plt.close()

    print("Backtesting completed")
