from fastapi import FastAPI
import random

app = FastAPI()

# --- Dummy Market Data ---
def get_data():
    return {
        "price": random.randint(23000, 24000),
        "vwap": random.randint(23000, 24000),
        "ema9": random.randint(23000, 24000),
        "ema21": random.randint(23000, 24000),
        "volume": random.randint(1000, 5000),
        "avg_volume": 3000,
        "pcr": round(random.uniform(0.5, 1.5), 2)
    }

# --- Signal Logic ---
def generate_signal(data):
    score = 0

    # VWAP
    if data["price"] > data["vwap"]:
        score += 2
    else:
        score -= 2

    # EMA
    if data["ema9"] > data["ema21"]:
        score += 2
    else:
        score -= 2

    # Volume
    if data["volume"] > data["avg_volume"]:
        score += 1

    # PCR
    if data["pcr"] > 1:
        score += 1
    elif data["pcr"] < 0.7:
        score -= 1

    # Final Signal
    if score >= 4:
        signal = "BUY CALL"
    elif score <= -4:
        signal = "BUY PUT"
    else:
        signal = "NO TRADE"

    return signal, score

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/signal")
def signal():
    data = get_data()
    signal, score = generate_signal(data)

    return {
        "index": "NIFTY",
        "ltp": data["price"],
        "vwap": data["vwap"],
        "ema9": data["ema9"],
        "ema21": data["ema21"],
        "volume": data["volume"],
        "pcr": data["pcr"],
        "signal": signal,
        "confidence": abs(score) * 20
    }
