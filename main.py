from flask import Flask, jsonify
import random
from engine import run_engine   # 🔥 IMPORT ENGINE

app = Flask(__name__)


# 🔥 DUMMY MARKET DATA (Replace later with Zerodha)
def get_market_data():
    return {
        "index": "NIFTY",
        "ltp": random.randint(23500, 24000),
        "vwap": random.randint(23500, 24000),
        "ema9": random.randint(23500, 24000),
        "ema21": random.randint(23500, 24000),
        "pcr": round(random.uniform(0.5, 1.5), 2),
        "volume": random.randint(500, 5000),
        "prev_high": 24000,
        "prev_low": 23500
    }


# 🔥 CONNECT ENGINE
def generate_signal(data):
    return run_engine(data)


# 🌐 API ROUTE
@app.route("/signal")
def signal():

    data = get_market_data()
    result = generate_signal(data)

    return jsonify({
        "index": data["index"],
        "ltp": data["ltp"],
        "vwap": data["vwap"],
        "ema9": data["ema9"],
        "ema21": data["ema21"],
        "pcr": data["pcr"],
        "volume": data["volume"],
        "signal": result.get("signal"),
        "confidence": result.get("confidence"),
        "entry": result.get("entry"),
        "sl": result.get("sl"),
        "target": result.get("target"),
        "score": result.get("score"),
        "reasons": result.get("reasons")
    })


# 🚀 RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)
