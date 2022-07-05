# Backtest


using MACD  
     ------------------------------ ANALYSIS ------------------------------  


Sharpe Ratio: 0.18474054151509864  

            ---------- Returns ----------  
rtot : 0.5794905526856564  
ravg : 8.866134527014327e-05  
rnorm : 0.022594125531969208  
rnorm100 : 2.259412553196921  

            ---------- DrawDowns ----------  
len : 17  
drawdown : 3.9841601535824123  
moneydown : 7407.359999999986  
len : 1941  
drawdown : 20.10887216259111  
moneydown : 28152.988499999978  


Final Portfolio Value: 178512.88  


using Stoch RSI   
     ------------------------------ ANALYSIS ------------------------------  


Sharpe Ratio: 0.3176636824413759  

            ---------- Returns ----------  
rtot : 2.168079275486048  
ravg : 0.0003317134754415618  
rnorm : 0.08718500974242484  
rnorm100 : 8.718500974242485  

            ---------- DrawDowns ----------  
len : 1696  
drawdown : 18.621164594995527  
moneydown : 200023.137  
len : 1882  
drawdown : 87.94382301523287  
moneydown : 944666.9820000001  


Final Portfolio Value: 874147.79  


using Bollinger Bands    
     ------------------------------ ANALYSIS ------------------------------  


Sharpe Ratio: 0.31959245497586675  

            ---------- Returns ----------  
rtot : 1.5859707499229714  
ravg : 0.0002426515835255464  
rnorm : 0.06305644646764198  
rnorm100 : 6.305644646764199  

            ---------- DrawDowns ----------  
len : 17  
drawdown : 13.662482767185145  
moneydown : 77287.35000000003  
len : 1281  
drawdown : 37.89647491469678  
moneydown : 206955.89249999996  


Final Portfolio Value: 488403.03  




The repo contains simple strategies backtesting examples using Backtrader in Python.  
https://www.backtrader.com/docu/quickstart/quickstart/



The data used is Tatamotars historical data from yahoo finance.  



I have used 3 simple strategies  
-RSI  https://www.investopedia.com/terms/r/rsi.asp  
-Bollinger's Band  https://www.investopedia.com/articles/technical/102201.asp   
-MACD Crossover  https://www.investopedia.com/trading/macd/  
