import backtrader as bt
import math


class Sizer(bt.Sizer):
    params = (
        ('risk', 0.003),
    )
    
    def __init__(self) -> None:
       super().__init__()
       if self.p.risk is None:
           self.p.risk = 0.003
       elif self.p.risk < 0:
           raise ValueError('Risk must be positive')
          

    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            return math.floor((cash-(cash*self.p.risk)) / data.close[0])
        else:
            return self.broker.getposition(data).size