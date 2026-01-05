import json
import os
from store.market_store import get_ltp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

def load_weights():
    with open(os.path.join(CONFIG_DIR, "nifty50.json")) as f:
        return json.load(f)

def load_previous_close():
    with open(os.path.join(CONFIG_DIR, "previous_close.json")) as f:
        return json.load(f)

def calculate_contribution():
    weights = load_weights()
    previous_close = load_previous_close()
    ltp_data = get_ltp()

    if not ltp_data:
        return {"pullers": [], "draggers": [], "net_contribution": 0.0 , "status": "Market is closed or no live data available"}

    pullers = []
    draggers = []
    net_contribution = 0.0

    for symbol, info in weights.items():
        token = str(info["token"])
        weight = info["weight"]

        if token not in ltp_data:
            continue

        ltp = ltp_data[token]

        if symbol not in previous_close or previous_close[symbol] == 0:
            continue

        prev = previous_close[symbol]

        price_change = ltp - prev
        percent_change = price_change / prev
        contribution = percent_change * weight 
# changed 
        stock_data = {
            "symbol": symbol,
            "ltp": round(ltp, 2),
            "change": round(price_change, 2),
            "percent": round(percent_change * 100, 2),
            "contribution": round(contribution, 4)
        }

        net_contribution += contribution

        if contribution >= 0:
            pullers.append(stock_data)
        else:
            draggers.append(stock_data)

    pullers.sort(key=lambda x: x["contribution"], reverse=True)
    draggers.sort(key=lambda x: x["contribution"])

    return {
        "pullers": pullers,   # top 10 pullers
        "draggers": draggers, # top 10 draggers
        "net_contribution": round(net_contribution, 4)
    }




