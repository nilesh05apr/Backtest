from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats

import pandas as pd
import matplotlib.pyplot as plt

class BBandStrategy(bt.Strategy):
      def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        size = self.getposition().size
        print('%s, %s CURRENT POSITION %s' % (dt.isoformat(), txt, size))

      def __init__(self):
        self.bband = bt.indicators.BollingerBands(period = 20, devfactor = 2)
        self.order = False
      
      def next(self):
        buy = self.data.close > self.bband.lines.top
        sell = self.data.close < self.bband.lines.bot
        if buy:
          self.log('BUY CREATE AT PRICE , %.2f' % self.data.close[0])
          self.buy()
          self.order = True
        elif sell and self.order:
          self.log('SELL CREATE AT PRICE , %.2f' % self.data.close[0])
          self.sell(size=self.getposition().size)
          self.order = False




cb = bt.Cerebro()
cb.addstrategy(BBandStrategy)
data = bt.feeds.YahooFinanceCSVData(dataname = '../data/TATAMOTORS.NS.csv')
cb.adddata(data)
cb.broker.setcash(100000.0)
cb.broker.setcommission(commission=0.001)
cb.addsizer(bt.sizers.FixedSize, stake=150)
print('Starting Portfolio Value: %.2f' % cb.broker.getvalue())
cb.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe_ratio')
cb.addanalyzer(btanalyzers.Returns, _name='returns')
cb.addanalyzer(btanalyzers.DrawDown, _name='draw_down')
thestrats = cb.run()
thestrat = thestrats[0]


print('\n\n','-'*30,'ANALYSIS','-'*30)
print('\n')
sharperatio = thestrat.analyzers.sharpe_ratio.get_analysis()
sharperatio = list(sharperatio.items())[0]
print('Sharpe Ratio:', sharperatio[1])
print('\n',' '*10,'-'*10,'Returns','-'*10)
returns = thestrat.analyzers.returns.get_analysis()
returns = list(returns.items())
for k,v in returns:
    print(k,':',v)
print('\n',' '*10,'-'*10,'DrawDowns','-'*10)
drawdown = thestrat.analyzers.draw_down.get_analysis()
drawdown = list(drawdown.items())
for k,v in drawdown:
    if k == 'max':
        max = list(v.items())
        for k2,v2 in max:
            print(k2,':',v2)
    else:
        print(k,':',v)
print('\n')
print('Final Portfolio Value: %.2f' % cb.broker.getvalue())
