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


# Create a Stratey
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 20),
        ('printlog', False),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            size = self.getposition().size
            print('%s, %s CURRENT POSITION %s' % (dt.isoformat(), txt,size))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)









cb = bt.Cerebro()
cb.addstrategy(TestStrategy)
data = bt.feeds.YahooFinanceCSVData(dataname = '../data/TATAMOTORS.NS.csv')
cb.adddata(data)
#cb.addsizer(bt.sizers.FixedSize, stake=10)
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








