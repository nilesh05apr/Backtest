from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt

class BBandStrategy(bt.Strategy):
      def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

      def __init__(self):
        self.bband = bt.indicators.BollingerBands(period = 20, devfactor = 2)
        self.order = False
      
      def next(self):
        buy = self.data.close > self.bband.lines.top
        sell = self.data.close < self.bband.lines.bot
        if buy and not self.order:
          self.log('BUY CREATE, %.2f' % self.data.close[0])
          self.buy()
          self.order = True
        elif sell and self.order:
          self.log('SELL CREATE, %.2f' % self.data.close[0])
          self.sell()
          self.order = False


cb = bt.Cerebro()
cb.addstrategy(BBandStrategy)
data = bt.feeds.YahooFinanceCSVData(dataname = 'TATAMOTORS.NS.csv')
cb.adddata(data)
cb.broker.setcash(100000.0)
print('Starting Portfolio Value: %.2f' % cb.broker.getvalue())
cb.run()
print('Final Portfolio Value: %.2f' % cb.broker.getvalue())
figure = plt.gcf()
figure.set_size_inches(10,5)
cb.plot()[0][0].savefig('BollingerBnads.png', dpi=300)