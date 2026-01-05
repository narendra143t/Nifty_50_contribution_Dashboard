# ltp_data = {}

# def update_ltp(token, ltp):
#     ltp_data[token] = ltp

# def get_ltp(token):
#     return ltp_data.get(token)


# store/market_store.py
ltp_data = {}

def update_ltp(token, ltp):
    global ltp_data
    ltp_data[token] = ltp

def get_ltp():
    global ltp_data
    return ltp_data
