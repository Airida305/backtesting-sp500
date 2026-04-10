## Raid Group for backtesting-SP500
| User | Role | Assessment |
|------|------|------------|
| Rustem Satimov | Leader | TBD |
| Aigerim Akhmetova | Member | TBD |

## Main goal
Prepare sp500 sonstituents (500 largest companies) dataset for a backtest.
## Project structure

## Environment setting, possible starting cmds

## Data
| File name | Description |
|-----------|-------------|
| sp500.csv | List of 500 largest companies in the US stock market, with their ticker symbols and other relevant information. |
| stock_prices.csv | Historical stock price data for the companies in the S&P 500 index, including daily open, high, low, close prices, and trading volume. |
## Description of files content.
### main.py
### backtester.py
### create_signal.py
### preprocessing.py
### memory_reducer.py

## Strategy
### Айгерим если есть крутые стратегии просто пиши тут
### Signals
### Benchmark (Выбор акции?) 20 по monthly average.

## Metrics
### Risk-adjustments returns (Sharpe ratio, Sortino ratio)
### Maximum drawdown
### Volatility
### Cumulative returns
### Alpha and Beta
### Win rate and loss rate
### Average gain and average loss
### Calmar ratio

## Question raised during the project
### 1. Почему мы выбрали именно эти метрики для оценки стратегии? Какие из них наиболее важные для нашего конкретного случая?
### 2. Как мы будем обрабатывать пропущенные данные в нашем наборе данных?
### 3. Какие методы оптимизации мы будем использовать для улучшения производительности нашего бэктестера?
### 4. Как мы будем учитывать изменения в составе S&P 500 (компании могут входить и выходить из индекса) при проведении бэктеста?
### 5. Нужен ли нам использовать какие-то дополнительные данные (например, макроэкономические показатели) для улучшения нашей стратегии?

### Robust approach we chose to overhead this project:
1...
2...
3...
