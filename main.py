from flask import Flask, jsonify
from engine import run_engine
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "API is running 🚀"


@app.route("/signal")
def signal():

    # Dummy Data
    data = {
        "price": 22450,
        "vwap": 22420,
        "ema_9": 22460,
        "ema_21": 22430,
        "pcr": 1.1,
        "volume": 120000,
        "avg_volume": 100000,
        "support": 22400,
        "resistance": 22500,

        # Structure
        "hh": True,
        "hl": True,
        "lh": False,
        "ll": False,

        # ORB
        "orb_high": 22480,
        "orb_low": 22380
    }

    result = run_engine(data)

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
