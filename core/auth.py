import os
import pyotp
from dotenv import load_dotenv
from SmartApi import SmartConnect
from utils.logger import logger

# LOAD .env FROM PROJECT ROOT
load_dotenv()

def login():
    logger.info("Logging into SmartAPI")

    api_key = os.getenv("API_KEY")
    client_code = os.getenv("CLIENT_CODE")
    password = os.getenv("PASSWORD")
    totp_secret = os.getenv("TOTP_SECRET")

    # 🔒 HARD VALIDATION
    if not api_key:
        raise Exception("API_KEY missing in .env")
    if not client_code:
        raise Exception("CLIENT_CODE missing in .env")
    if not password:
        raise Exception("PASSWORD missing in .env")
    if not totp_secret:
        raise Exception("TOTP_SECRET missing in .env")

    totp = pyotp.TOTP(totp_secret).now()

    smart_api = SmartConnect(api_key)
    session = smart_api.generateSession(client_code, password, totp)

    if not session.get("status"):
        raise Exception(f"SmartAPI login failed: {session}")

    smart_api.authToken = session["data"]["jwtToken"]
    smart_api.feedToken = session["data"]["feedToken"]
    smart_api.client_code = client_code

    logger.info("SmartAPI login successful")
    return smart_api
