import requests, json, time

# ---------- NIFTY 50 SYMBOLS ----------
nifty50_symbols = [
    
    "RELIANCE", "HDFCBANK", "TCS", "INFY", "ICICIBANK", "LT","BHARTIARTL", "M%26M","ITC","SBIN", "AXISBANK",

    "HINDUNILVR",  "AXISBANK", "BAJFINANCE", "MARUTI",
    "ASIANPAINT", "SUNPHARMA", "WIPRO",  "TITAN", "TATASTEEL", 
    "POWERGRID", "ADANIPORTS", "JSWSTEEL", "ULTRACEMCO",
    "HEROMOTOCO", "HCLTECH", "TECHM","BAJAJ-AUTO",
  "COALINDIA",
    "GRASIM", "ONGC", "NESTLEIND", "HINDALCO", "EICHERMOT",
    "DRREDDY", "BAJAJFINSV", "SBILIFE",  "HDFCLIFE",
    "ADANIENT", "CIPLA", "TATACONSUM", "APOLLOHOSP", "NTPC", "INDUSINDBK","KOTAKBANK","BEL",
"ETERNAL",
"IOC",
"JIOFIN",
"SHRIRAMFIN",
"TATAMOTORS",
"TRENT"

]

# ---------- FETCH PC FROM NSE ----------
def get_prev_close(symbol):
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "accept": "application/json"
    }
    r = requests.get(url, headers=headers)
    data = r.json()
    return data["priceInfo"]["previousClose"]

previous_close_map = {}

# ---------- FETCH FOR ALL SYMBOLS ----------
for sym in nifty50_symbols:
    try:
        pc = get_prev_close(sym)
        previous_close_map[sym] = pc
        print(sym, pc)
        time.sleep(0.3)   # avoid blocking
    except Exception as e:
        print("Error fetching:", sym, e)

# ---------- SAVE TO JSON ----------
with open("previous_close.json", "w") as f:
    json.dump(previous_close_map, f, indent=4)

print("\nSaved previous_close.json successfully!")
