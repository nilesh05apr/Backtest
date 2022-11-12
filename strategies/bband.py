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



