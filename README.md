# Backtest

Backtesting is a key component of effective trading system development. It is accomplished by reconstructing, with historical data, trades that would have occurred in the past using rules defined by a given strategy. The result offers statistics to gauge the effectiveness of the strategy.   

## Dataset  

The project is built using TATAMOTORS share price data for 20 years  

For custom dataset place the csv file in /data directory and change input_file_path='custom data.csv'

## Run Locally  

Clone the project    

```bash
  git clone https://github.com/nilesho5apr/Backtest.git
```
Go to the project directory  

```bash
  cd Backtest
```
Create virtual enviroment  

```bash
  virtualenv venv
```

Install dependencies  

```bash
  python3 -m pip install -r requirements.txt
```


Run simulations  

```bash
  python3 main.py --arguments
```

## Documentation  

[Backtrader](https://www.backtrader.com/docu/quickstart/quickstart/)
