from flask import Flask, jsonify
from engine import run_engine
from candle_builder import CandleBuilder  # ✅ NEW
import os
import random

app = Flask(__name__)

# ✅ Create candle builder instance
builder = CandleBuilder(duration=30)


@app.route("/")
def home():
    return "API is running 🚀"


@app.route("/signal")
def signal():

    # 🔥 Simulate live price movement
    price = 22400 + random.randint(-50, 50)

    # 🔥 Update candle with new price
    builder.update(price)

    current_candle, prev_candle = builder.get_candles()

    # Handle first run (no previous candle)
    if not prev_candle:
        prev_candle = current_candle

    # 🔥 Prepare data for engine
    data = {
        "price": price,
        "vwap": price - 20,
        "ema_9": price + 10,
        "ema_21": price - 10,
        "pcr": 1.1,
        "volume": random.randint(90000, 150000),
        "avg_volume": 100000,
        "support": price - 80,
        "resistance": price + 80,

        # Structure
        "hh": True,
        "hl": True,
        "lh": False,
        "ll": False,

        # ORB
        "orb_high": price + 40,
        "orb_low": price - 40,

        # 🔥 Dynamic candle data
        "candle_5m": current_candle,
        "prev_candle_5m": prev_candle,

        # 🔥 Simple trend logic (temporary)
        "candle_15m_trend": "BULLISH" if price > (price - 20) else "BEARISH"
    }

    # Run engine
    result = run_engine(data)

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
