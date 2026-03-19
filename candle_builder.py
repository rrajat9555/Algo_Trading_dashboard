import time

class CandleBuilder:

    def __init__(self, duration=30):  # 30 sec = demo (later 300 for 5 min)
        self.current_candle = None
        self.prev_candle = None
        self.start_time = time.time()
        self.duration = duration

    def update(self, price):

        now = time.time()

        # 🔥 Check if candle time is over
        if now - self.start_time >= self.duration:
            self.close_candle()
            self.start_time = now

        # Create new candle if none
        if not self.current_candle:
            self.current_candle = {
                "open": price,
                "high": price,
                "low": price,
                "close": price
            }
            return

        # Update current candle
        self.current_candle["high"] = max(self.current_candle["high"], price)
        self.current_candle["low"] = min(self.current_candle["low"], price)
        self.current_candle["close"] = price

    def close_candle(self):
        if self.current_candle:
            self.prev_candle = self.current_candle
        self.current_candle = None

    def get_candles(self):
        return self.current_candle, self.prev_candle
