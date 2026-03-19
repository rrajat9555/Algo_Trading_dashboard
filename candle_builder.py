class CandleBuilder:

    def __init__(self):
        self.current_candle = None
        self.prev_candle = None

    def update(self, price):

        if not self.current_candle:
            self.current_candle = {
                "open": price,
                "high": price,
                "low": price,
                "close": price
            }
            return

        self.current_candle["high"] = max(self.current_candle["high"], price)
        self.current_candle["low"] = min(self.current_candle["low"], price)
        self.current_candle["close"] = price

    def close_candle(self):
        self.prev_candle = self.current_candle
        self.current_candle = None

    def get_candles(self):
        return self.current_candle, self.prev_candle