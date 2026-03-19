# engine.py

def vwap_strategy(data):
    if data["price"] > data["vwap"]:
        return {"signal": "CALL", "score": 1}
    elif data["price"] < data["vwap"]:
        return {"signal": "PUT", "score": 1}
    return {"signal": "NEUTRAL", "score": 0}


def ema_strategy(data):
    if data["ema_9"] > data["ema_21"]:
        return {"signal": "CALL", "score": 1}
    elif data["ema_9"] < data["ema_21"]:
        return {"signal": "PUT", "score": 1}
    return {"signal": "NEUTRAL", "score": 0}


def pcr_strategy(data):
    if data["pcr"] > 1.2:
        return {"signal": "CALL", "score": 1}
    elif data["pcr"] < 0.8:
        return {"signal": "PUT", "score": 1}
    return {"signal": "NEUTRAL", "score": 0}


def volume_strategy(data):
    if data["volume"] > data["avg_volume"]:
        return {"signal": "CONFIRM", "score": 1}
    return {"signal": "WEAK", "score": 0}
