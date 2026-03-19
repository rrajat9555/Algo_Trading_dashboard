# engine.py

# =========================
# STRATEGIES
# =========================

def vwap_strategy(data):
    if data["price"] > data["vwap"]:
        return {"signal": "CALL", "score": 2}
    elif data["price"] < data["vwap"]:
        return {"signal": "PUT", "score": 2}
    return {"signal": "NEUTRAL", "score": 0}


def ema_strategy(data):
    if data["ema_9"] > data["ema_21"]:
        return {"signal": "CALL", "score": 2}
    elif data["ema_9"] < data["ema_21"]:
        return {"signal": "PUT", "score": 2}
    return {"signal": "NEUTRAL", "score": 0}


def pcr_strategy(data):
    if data["pcr"] > 1.2:
        return {"signal": "CALL", "score": 1}
    elif data["pcr"] < 0.8:
        return {"signal": "PUT", "score": 1}
    return {"signal": "NEUTRAL", "score": 0}


def breakout_strategy(data):
    if data["price"] > data["resistance"]:
        return {"signal": "CALL", "score": 3}
    elif data["price"] < data["support"]:
        return {"signal": "PUT", "score": 3}
    return {"signal": "NEUTRAL", "score": 0}


def volume_strategy(data):
    if data["volume"] > data["avg_volume"]:
        return {"signal": "STRONG"}
    return {"signal": "WEAK"}


def structure_strategy(data):
    if data["hh"] and data["hl"]:
        return {"signal": "CALL", "score": 2}
    elif data["lh"] and data["ll"]:
        return {"signal": "PUT", "score": 2}
    return {"signal": "NEUTRAL", "score": 0}


def orb_strategy(data):
    if data["price"] > data["orb_high"]:
        return {"signal": "CALL", "score": 2}
    elif data["price"] < data["orb_low"]:
        return {"signal": "PUT", "score": 2}
    return {"signal": "NEUTRAL", "score": 0}


def trap_strategy(data):
    if data["price"] > data["resistance"] and data["volume"] < data["avg_volume"]:
        return "FAKE_BREAKOUT"

    if data["price"] < data["support"] and data["volume"] < data["avg_volume"]:
        return "FAKE_BREAKDOWN"

    return "SAFE"


# =========================
# MAIN ENGINE
# =========================

def run_engine(data):

    # 1. Trap detection (FIRST)
    trap = trap_strategy(data)
    if trap != "SAFE":
        return {
            "signal": "NO TRADE",
            "reason": trap,
            "confidence": 0
        }

    # 2. Run strategies
    strategies = [
        vwap_strategy(data),
        ema_strategy(data),
        structure_strategy(data),
        breakout_strategy(data),
        orb_strategy(data),
        pcr_strategy(data)
    ]

    call_score = 0
    put_score = 0

    for s in strategies:
        if s["signal"] == "CALL":
            call_score += s["score"]
        elif s["signal"] == "PUT":
            put_score += s["score"]

    # 3. Volume confirmation
    volume = volume_strategy(data)
    if volume["signal"] == "WEAK":
        return {
            "signal": "NO TRADE",
            "reason": "LOW VOLUME",
            "confidence": 0
        }

    # 4. Final decision
    total_possible = 12  # max score

    if call_score > put_score:
        signal = "BUY CALL"
        confidence = (call_score / total_possible) * 100

    elif put_score > call_score:
        signal = "BUY PUT"
        confidence = (put_score / total_possible) * 100

    else:
        signal = "NO TRADE"
        confidence = 0

    return {
        "signal": signal,
        "confidence": round(confidence, 2),
        "call_score": call_score,
        "put_score": put_score
    }
