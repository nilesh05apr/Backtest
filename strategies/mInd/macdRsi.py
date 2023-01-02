import backtrader as bt


class MACDRSI(bt.Strategy):
    params = (
        ('period', 14),
        ('rsi_period', 14),
        ('rsi_upper', 70),
        ('rsi_lower', 30),
        ('rsi_overbought', 70),
        ('rsi_oversold', 30),
        ('macd1', 12),
        ('macd2', 26),
        ('macd_signal', 9),
        ('printlog', False),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.p.rsi_period)
        self.macd = bt.indicators.MACDHisto(self.data, period_me1=self.p.macd1, period_me2=self.p.macd2, period_signal=self.p.macd_signal)
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' % (order.executed.price, order.executed.value, order.executed.comm))
            elif order.issell():
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' % (order.executed.price, order.executed.value, order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.rsi < self.p.rsi_lower and self.macd.macd > self.macd.signal:
                self.log('BUY CREATE, %.2f' % self.data.close[0])
                self.order = self.buy()
        else:
            if self.rsi > self.p.rsi_upper and self.macd.macd < self.macd.signal:
                self.log('SELL CREATE, %.2f' % self.data.close[0])
                self.order = self.sell()


