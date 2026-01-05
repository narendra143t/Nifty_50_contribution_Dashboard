import time
from store.market_store import update_ltp
from engine.contribution_engine import calculate_contribution

# Example token → symbol mapping (same as nifty50.json)
tokens = {
    "2885": "RELIANCE",
    "1594": "INFY",
    "4963": "ICICIBANK",
    "1333": "HDFCBANK",
    "10999": "TCS"
}

# Simulate live LTPs
ltp_values = {
    "2885": 2500,
    "1594": 1700,
    "4963": 635,
    "1333": 985,
    "10999": 3300
}

try:
    while True:
        # Update LTPs randomly (+/- small amount)
        for token in tokens:
            ltp_values[token] += (-5 + 10 * time.time() % 1)  # small variation
            update_ltp(token, ltp_values[token])

        # Calculate contributions
        data = calculate_contribution()

        # Print results
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
    print("Exiting simulation...")
