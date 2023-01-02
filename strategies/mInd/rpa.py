import backtrader as bt


class TestStrategy(bt.Strategy):
    params = (
        ('period', 14),

    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        size = self.getposition().size
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s CURRENT POSITION : %s' % (dt.isoformat(), txt, size))

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order_exist = False
        self.rsi = bt.indicators.RSI(self.data, period=self.p.period)
        self.psar = bt.indicators.ParabolicSAR(self.data)
        self.atr = bt.indicators.ATR(self.data)
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, PRICE : %.2f, COST : %.2f, COMMISSION : %.2f' % (order.executed.price, order.executed.value, order.executed.comm))
            elif order.issell():
                self.log('SELL EXECUTED, PRICE : %.2f, COST : %.2f, COMMISSION : %.2f' % (order.executed.price, order.executed.value, order.executed.comm))

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('ORDER CANCELED/MARGIN/REJECTED')

        self.order = None
    
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))

    def next(self):
        # self.log('CLOSE PRICE : %.2f,' % self.dataclose[0])
        # self.log('CURRENT RSI : %.2f, CURRENT PSAR : %.2f, CURRENT ATR : %.2f' % (self.rsi[0], self.psar[0], self.atr[0]))

        if self.order:
            return
        
        if not self.position:
            if self.dataclose[0] > self.psar[0]:
                self.log('PRICE ABOVE PSAR')
                sell_signal = self.rsi > 70 or self.atr > self.dataclose[0]
                if self.order_exist and sell_signal:
                    self.log('SELL CREATE AT PRICE : %.2f,' % self.dataclose[0])
                    self.order = self.sell()
                    self.order_exist = False

            else:
                self.log('PRICE BELOW PSAR')
                buy_signal = self.rsi < 30 or self.atr < self.dataclose[0]
                if buy_signal:
                    self.log('BUY CREATE AT PRICE : %.2f,' % self.dataclose[0])
                    self.order = self.buy()
                    self.order_exist = True

        