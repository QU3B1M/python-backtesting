import backtrader as bt
from indicators.trix_signal import TrixIndicator


class TestStrategy(bt.Strategy):
    params = (("trixperiod", 15),)

    def log(self, txt, dt=None):
        """ Logging function fot this strategy"""
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
        # We are only using this indicator for the Plot, not to buy or sell
        TrixIndicator(self.data, period=self.params.trixperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED {order.executed.price}")
            if order.issell():
                self.log(f"SELL EXECUTED {order.executed.price}")
            self.bar_executed = len(self)

        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log("Close, %.2f" % self.dataclose[0])

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log("BUY CREATE, %.2f" % self.dataclose[0])
                    self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                self.log(f"SELL CREATED {self.dataclose[0]}")
                self.order = self.sell()
