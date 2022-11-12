import backtrader as bt


class ADX(bt.Indicator):
    lines = ('adx',)
    params = dict(
        period=14,
    )

    def __init__(self):
        self.adx = bt.indicators.AverageDirectionalMovementIndex(self.data, period=self.p.period)
        self.lines.adx = self.adx.lines.adx

    
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        size = self.getposition().size
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s CURRENT POSITION : %s' % (dt.isoformat(), txt, size))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.adx_indicator = ADX()
        self.order_exist = False

    def next(self):
      previous_adx = self.adx_indicator.lines.adx[-1]
      current_adx = self.adx_indicator.lines.adx[0]
      buy_signal = previous_adx <  current_adx and current_adx < 20
      sell_signal = previous_adx > current_adx and current_adx > 50


      if buy_signal:
        self.log('BUY CREATE AT PRICE : %.2f,' % self.dataclose[0])
        self.buy()
        self.order_exist = True
      elif sell_signal and self.order_exist:
        self.log('SELL CREATE AT PRICE : %.2f,' % self.dataclose[0])
        self.sell()
        self.order_exist = False