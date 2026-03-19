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
# CANDLE STRATEGIES (NEW)
# =========================

def momentum_candle(data):
    body = abs(data["close"] - data["open"])
    range_ = data["high"] - data["low"]

    if range_ == 0:
        return {"signal": "NEUTRAL", "score": 0}

    body_percent = body / range_

    if body_percent > 0.7:
        if data["close"] > data["open"]:
            return {"signal": "CALL", "score": 2}
        else:
            return {"signal": "PUT", "score": 2}

    return {"signal": "NEUTRAL", "score": 0}


def rejection_candle(data):
    upper_wick = data["high"] - max(data["open"], data["close"])
    lower_wick = min(data["open"], data["close"]) - data["low"]
    body = abs(data["close"] - data["open"])

    if body == 0:
        body = 1

    if lower_wick > body * 2:
        return {"signal": "CALL", "score": 1}

    if upper_wick > body * 2:
        return {"signal": "PUT", "score": 1}

    return {"signal": "NEUTRAL", "score": 0}


def engulfing_candle(data):
    prev_open = data["prev_open"]
    prev_close = data["prev_close"]

    if data["close"] > data["open"] and prev_close < prev_open:
        if data["close"] > prev_open and data["open"] < prev_close:
            return {"signal": "CALL", "score": 2}

    if data["close"] < data["open"] and prev_close > prev_open:
        if data["open"] > prev_close and data["close"] < prev_open:
            return {"signal": "PUT", "score": 2}

    return {"signal": "NEUTRAL", "score": 0}


# =========================
# RANGE FILTER
# =========================

def range_filter(data):
    range_size = data["resistance"] - data["support"]

    if range_size < 50:
        return True
    return False


# =========================
# MAIN ENGINE
# =========================

def run_engine(data):

    # 0. Range filter
    if range_filter(data):
        return {
            "signal": "NO TRADE",
            "reason": "SIDEWAYS MARKET",
            "confidence": 0
        }

    # 1. Trap detection
    trap = trap_strategy(data)
    if trap != "SAFE":
        return {
            "signal": "NO TRADE",
            "reason": trap,
            "confidence": 0
        }

    # 2. Run strategies (INCLUDING CANDLES)
    strategies = [
        vwap_strategy(data),
        ema_strategy(data),
        structure_strategy(data),
        breakout_strategy(data),
        orb_strategy(data),
        pcr_strategy(data),

        # Candle intelligence
        momentum_candle(data),
        rejection_candle(data),
        engulfing_candle(data)
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
    total_possible = 18  # updated
    MIN_CONFIDENCE = 60

    if call_score > put_score:
        confidence = (call_score / total_possible) * 100

        if confidence < MIN_CONFIDENCE:
            return {
                "signal": "NO TRADE",
                "confidence": round(confidence, 2),
                "reason": "LOW CONFIDENCE"
            }

        signal = "BUY CALL"

    elif put_score > call_score:
        confidence = (put_score / total_possible) * 100

        if confidence < MIN_CONFIDENCE:
            return {
                "signal": "NO TRADE",
                "confidence": round(confidence, 2),
                "reason": "LOW CONFIDENCE"
            }

        signal = "BUY PUT"

    else:
        signal = "NO TRADE"
        confidence = 0

    return {
        "signal": signal,
        "confidence": round(confidence, 2),
        "call_score": call_score,
        "put_score": put_score
    }
