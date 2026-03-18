from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/signal")
def get_signal():
    signals = ["BUY CALL", "BUY PUT", "NO TRADE"]
    
    return {
        "index": "NIFTY",
        "ltp": random.randint(23000, 24000),
        "signal": random.choice(signals),
        "strike": "23750 CE",
        "confidence": random.randint(60, 90)
    }