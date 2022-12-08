# Import the backtrader platform
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats
import pandas as pd
import matplotlib.pyplot as plt


class KDJ(bt.Indicator):
    lines = ('k', 'd', 'j')
    params = dict(
        period=14,  # to apply to RSI
        pperiod=None,  # if passed apply to HighestN/LowestN, else "period"
    )

    def __init__(self):
        pperiod = self.p.pperiod or self.p.period
        rsv = (self.data - bt.ind.Lowest(self.data, period=pperiod)) / (bt.ind.Highest(self.data, period=pperiod) - bt.ind.Lowest(self.data, period=pperiod))
        self.l.k = bt.ind.SMA(rsv, period=3)
        self.l.d = bt.ind.SMA(self.l.k, period=3)
        self.l.j = 3 * self.l.k - 2 * self.l.d

class KDJStrategy(bt.Strategy):
    params = dict(
        period=14,  # to apply to RSI
        pperiod=None,  # if passed apply to HighestN/LowestN, else "period"
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        size = self.getposition().size
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s CURRENT POSITION : %s' % (dt.isoformat(), txt, size))

    def __init__(self):
        self.kdj = KDJ(period=self.p.period, pperiod=self.p.pperiod)
        self.dataclose = self.datas[0].close
        self.order_exist = False

    def next(self):

        buy_signal = self.kdj.j < 20 and self.kdj.k > self.kdj.d
        sell_signal = self.kdj.j > 80 and self.kdj.k < self.kdj.d

        if buy_signal:
            self.log('BUY CREATE AT PRICE : %.2f,' % self.dataclose[0])
            self.buy()
            self.order_exist = True
        elif sell_signal and self.order_exist:
            self.log('SELL CREATE AT PRICE : %.2f,' % self.dataclose[0])
            self.sell()
            self.order_exist = False
    

