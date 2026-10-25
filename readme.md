## Raid Group for backtesting-SP500
___

## Main goal
Цель этого проекта — подготовить исторические данные по компаниям, входившим в S&P 500, для бэктеста и оценить простую стратегию выбора акций по сравнению с бенчмарком S&P 500.

Проект охватывает весь пайплайн:

1) загрузка исходных CSV-файлов,
2) оптимизация использования памяти,
3) очистка и предобработка финансовых временных рядов,
4) создание инвестиционного сигнала,
5) проведение бэктеста стратегии,
6) сравнение с бенчмарком S&P 500,
7) сохранение численных результатов и графиков.

Этот проект сосредоточен на надежной обработке данных и честном бэктесте на “грязных” финансовых данных.
___

## How to run the project from an empty environment
1) Создать и активировать виртуальное окружение
```
python3 -m venv .venv
source .venv/bin/activate
```
2) Обновить pip
```
python -m pip install --upgrade pip
```
3) Установить зависимости
```
pip install -r requirements.txt
```
4) Запустить полный пайплайн
```
python ./scripts/main.py
```
5) results/plots
    для .png графиков доходности и Quantative EDA
6) results/results.txt
    для численных результатов по стратегии и бенчмарку
7) results/outliers.txt
    для списка(5) подтвержденных выбросов
8) notebook/analysis.ipynb
    для EDA и анализа выбросов/стратегии1-2
____

## Project structure
```
project
│   README.md
│   requirements.txt
│
└───data                   Входные данные
│   │   sp500.csv          
│   |   stock_prices.csv
│
└───notebook
│   │   analysis.ipynb     EDA и анализ
|
|───scripts
|   │   memory_reducer.py  Чтение cvs, уменьшение потребления памяти, возврат DataFrame
|   │   preprocessing.py   Логика:очистка данных, ресемплинг по месяцам, фильтрация выбрасов, расчеты monthly_past_return и monthly_future_return
|   │   create_signal.py   Расчет average_return_1y, Signal, выбор top 10-20 акций
|   |   backtester.py      Расчет PnL стратегии, PnL benchmark, total return, сохранение результатов
│   |   main.py            Запуск проекта
│
└───results                Выходные данные
    │   plots
    │   results.txt
    │   outliers.txt       минимум 5 выбросов
```
## Expected outputs

## Environment setting, possible starting cmds

## Data
| File name | Description |
|-----------|-------------|
| sp500.csv | List of 500 largest companies in the US stock market, with their ticker symbols and other relevant information. |
| stock_prices.csv | Historical stock price data for the companies in the S&P 500 index, including daily open, high, low, close prices, and trading volume. |

## Strategy
### Выбранная стратегия:
Stock Picking / Cross-sectional momentum на месячных данных.
Каждый месяц мы смотрим на все акции, считаем для каждой сигнал на основе прошлых данных, выбираем 20 лучших акций и инвестируем по 1$ в каждую на следующий месяц. Общий объем инвестиций в месяц = 20$

### Сигнал

Сигнал строится только на основе monthly_past_return, как и требуется в проекте.

Для каждой компании и каждого месяца мы считаем:

1) сначала переводим цены в месячные и оставляем последнее значение месяца;

2) потом для каждой компании считаем:
average_return_1y = среднее значение предыдущих 12 monthly_past_return

3) затем внутри каждого месяца мы ранжируем все компании по average_return_1y.


### Итоговый столбец signal

Создаем булев столбец:
True — если акция входит в 20 самых высоких значений average_return_1y внутри этого месяца
False — если не входит
То есть отбор идет строго: top 20 компаний в месяц

### Метка/Целевая переменная /Будущий результат

Результативность стратегии оценивается через:
```
monthly_future_return​=(​price(t+1) ​− price(t​)​)/price(t)
```

### Benchmark

Бенчмарком выступает S&P 500.

Для него сравнения мы моделируем вторую стратегию, которая инвестирует: 20$ в S&P 500 каждый месяц.

## Ожидаемые результаты
После запуска проекта должны быть созданы или обновлены следующие файлы:

- В папке `results/` должны появиться или обновиться следующие файлы и папки:

    - **results.txt**  
        Содержит общий PnL и общую доходность для:
        - стратегии Stock Picking 20
        - бенчмарка S&P 500

    - **outliers.txt**  
        Список как минимум 5 подтвержденных выбросов в формате:
        - ticker
        - date
        - price

    - **График доходности**  
        Сохранён в `results/` (например, `results/performance.png`).

    - **Графики для raid TASKs/EDA**  
        Сохранены в папке `results/plots/` (например, `results/plots/eda_*.png`).

## Почему выбрана именно эта стратегия
Проект прямо требует использовать простой сигнал, основанный на прошлых доходностях.

Выбранная стратегия подходит, потому что:

- использует только ту информацию, которая была доступна в момент принятия решения,
- соответствует требованию проекта использовать monthly_past_return,
- её легко объяснить и проверять на аудите,
- это стандартный momentum-подход к выбору акций,
её можно напрямую сравнить с бенчмарком S&P 500.

