import backtrader as bt
import math


class GoldenCross(bt.Strategy):
    params = (
        ("fast", 50),
        ("slow", 200),
        ("order_percentage", 0.95),
        ("ticker", "SPY"),
    )

    def __init__(self):
        self.fast_moving_avergae = bt.indicators.SMA(
            self.data.close, period=self.params.fast, plotname="50 day moving average"
        )

        self.slow_moving_avergae = bt.indicators.SMA(
            self.data.close, period=self.params.slow, plotname="200 day moving average"
        )

        self.crossover = bt.indicators.CrossOver(
            self.fast_moving_avergae, self.slow_moving_avergae
        )

    def next(self):
        if self.position.size == 0 and self.crossover > 0:
            amount_to_invest = self.params.order_percentage + self.broker.cash
            self.size = math.floor(amount_to_invest / self.data.close)
            print(
                f"Buy {self.size} shares of {self.params.ticker} at {self.data.close[0]}"
            )
            self.buy(size=self.size)
        if self.position.size > 0 and self.crossover < 0:
            print(
                f"Sell {self.size} shares of {self.params.ticker} at {self.data.close[0]}"
            )
            self.close()
