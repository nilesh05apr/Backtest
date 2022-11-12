# Import the backtrader platform
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats
import pandas as pd
import matplotlib.pyplot as plt


class StochRSI(bt.Indicator):
    lines = ('stochrsi',)
    params = dict(
        period=14,  # to apply to RSI
        pperiod=None,  # if passed apply to HighestN/LowestN, else "period"
    )

    def __init__(self):
        rsi = bt.ind.RSI(self.data, period=self.p.period)

        pperiod = self.p.pperiod or self.p.period
        maxrsi = bt.ind.Highest(rsi, period=pperiod)
        minrsi = bt.ind.Lowest(rsi, period=pperiod)

        self.l.stochrsi = (rsi - minrsi) / (maxrsi - minrsi)


class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        size = self.getposition().size
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s CURRENT POSITION : %s' % (dt.isoformat(), txt, size))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.stochrsi_indicator = StochRSI()
        self.order_exist = False

    def next(self):
      previous_stochrsi = self.stochrsi_indicator.lines.stochrsi[-1]
      current_stochrsi = self.stochrsi_indicator.lines.stochrsi[0]
      buy_signal = previous_stochrsi <  current_stochrsi and current_stochrsi < 0.2
      sell_signal = previous_stochrsi > current_stochrsi and current_stochrsi > 0.8


      if buy_signal:
        self.log('BUY CREATE AT PRICE : %.2f,' % self.dataclose[0])
        self.buy()
        self.order_exist = True
      elif sell_signal and self.order_exist:
        self.log('SELL CREATE AT PRICE : %.2f,' % self.dataclose[0])
        self.sell()
        self.order_exist = False


