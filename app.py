# import json
# from core.auth import login
# from core.ltp_websocket import LTPWebSocket
# from utils.logger import logger
# import os
# from engine.contribution_engine import calculate_contribution


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# def load_tokens():
#     file_path = os.path.join(BASE_DIR, "config", "nifty50.json")
#     with open(file_path, "r") as f:
#         data = json.load(f)

#     tokens = [str(info["token"]) for info in data.values()]
#     return tokens  # <-- THIS WAS MISSING


# if __name__ == "__main__":
#     api = login()                 # login ONCE
#     tokens = load_tokens()        # read JSON

#     logger.info(f"Starting LTP for {len(tokens)} stocks")

#     ws = LTPWebSocket(api, tokens)
#     ws.start()


import json
import os
import time
from core.auth import login
from core.ltp_websocket import LTPWebSocket
from utils.logger import logger
from engine.contribution_engine import calculate_contribution

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# Load tokens from JSON
# -----------------------------
def load_tokens():
    file_path = os.path.join(BASE_DIR, "config", "nifty50.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    tokens = [str(info["token"]) for info in data.values()]
    return tokens

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    # 1️⃣ Login
    logger.info("Logging into SmartAPI...")
    api = login()
    logger.info("SmartAPI login successful.")

    # 2️⃣ Load tokens
    tokens = load_tokens()
    logger.info(f"Starting LTP feed for {len(tokens)} stocks")

    # 3️⃣ Start WebSocket
    ws = LTPWebSocket(api, tokens)
    ws.start()  # runs in background

    # 4️⃣ Contribution loop
    try:
        while True:
            data = calculate_contribution()

            # Market closed / no LTP data
            if not data["pullers"] and not data["draggers"]:
                logger.info("Market is closed or no live data available")
            else:
                # Display contributions
                print("\n=== Pullers ===")
                for s in data["pullers"]:
                    print(s)

                print("\n=== Draggers ===")
                for s in data["draggers"]:
                    print(s)

                print("Net Contribution:", data["net_contribution"])

            print("-" * 60)
            time.sleep(2)  # refresh interval

    except KeyboardInterrupt:
        logger.info("Exiting contribution dashboard...")
