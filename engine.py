def run_engine(data):

    score = 0
    reasons = []

    # ----------------------
    # 🔹 TREND ENGINE
    # ----------------------
    if data["ltp"] > data["vwap"]:
        score += 2
        reasons.append("Above VWAP")

    if data["ema9"] > data["ema21"]:
        score += 2
        reasons.append("EMA Bullish")

    # ----------------------
    # 🔹 VOLUME
    # ----------------------
    if data["volume"] > 1200:
        score += 1
        reasons.append("High Volume")

    # ----------------------
    # 🔹 PCR SENTIMENT
    # ----------------------
    if data["pcr"] > 1.1:
        score += 1
        reasons.append("Bullish PCR")
    elif data["pcr"] < 0.8:
        score -= 1
        reasons.append("Bearish PCR")

    # ----------------------
    # 🔹 SUPPORT / RESISTANCE FILTER
    # ----------------------
    if data["prev_low"] + 20 < data["ltp"] < data["prev_high"] - 20:
        return {
            "signal": "NO TRADE",
            "score": score,
            "reason": "Inside Range"
        }

    # ----------------------
    # 🔹 FINAL SIGNAL
    # ----------------------
    if score >= 4:
        signal = "BUY CALL"
    elif score <= -3:
        signal = "BUY PUT"
    else:
        signal = "NO TRADE"

    confidence = int((abs(score) / 6) * 100)

    return {
        "signal": signal,
        "score": score,
        "confidence": confidence,
        "reasons": reasons
    }