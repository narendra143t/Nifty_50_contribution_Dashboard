from flask import Flask, jsonify, render_template
from threading import Thread
import json
import os

from core.auth import login
from core.ltp_websocket import LTPWebSocket
from engine.contribution_engine import calculate_contribution
from utils.logger import logger

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

# -----------------------------
# Load tokens
# -----------------------------
def load_tokens():
    with open(os.path.join(CONFIG_DIR, "nifty50.json")) as f:
        data = json.load(f)
    return [str(info["token"]) for info in data.values()]

# -----------------------------
# WebSocket starter (background)
# -----------------------------
def start_websocket():
    logger.info("Logging into SmartAPI...")
    api = login()
    logger.info("SmartAPI login successful")

    tokens = load_tokens()
    logger.info(f"Starting WebSocket for {len(tokens)} tokens")

    ws = LTPWebSocket(api, tokens)
    ws.start()

# -----------------------------
# API Route
# -----------------------------
@app.route("/data")
def get_contribution_data():
    return jsonify(calculate_contribution())

@app.route("/dashboard")
def home():
    return render_template("index.html")

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    # Start WebSocket in background
    Thread(target=start_websocket, daemon=True).start()

    # Start Flask server
    app.run(host="0.0.0.0", port=5000, debug=True)

