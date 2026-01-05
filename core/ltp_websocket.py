from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from utils.logger import logger
from store.market_store import get_ltp, update_ltp


class LTPWebSocket:

    def __init__(self, api, tokens):
        self.api = api
        self.tokens = tokens
        self.ws = None

    def on_open(self, ws):
        logger.info("WebSocket connected")

        # ✅ SUBSCRIBE USING SmartWebSocketV2 OBJECT
        self.ws.subscribe(
            correlation_id="nifty_ltp",
            mode=1,  # 1 = LTP
            token_list=[{
                "exchangeType": 1,  # NSE
                "tokens": self.tokens
            }]
        )

        logger.info(f"Subscribed to {len(self.tokens)} tokens")

    def on_data(self, ws, message):
        try:
            token = message["token"]
            ltp = message["last_traded_price"] / 100
            # print(f"TOKEN {token} | LTP {ltp}")
            update_ltp(token, ltp)
            
           
        except Exception as e:
            logger.error(f"LTP parse error: {e}")
            
       

    def on_error(self, ws, error):
        logger.error(f"WebSocket error: {error}")

    def on_close(self, ws):
        logger.warning("WebSocket closed")

    def start(self):
        self.ws = SmartWebSocketV2(
        auth_token=self.api.authToken,    
        api_key=self.api.api_key,           
        client_code=self.api.client_code,   
        feed_token=self.api.feedToken      
        )

        # callbacks
        self.ws.on_open = self.on_open
        self.ws.on_data = self.on_data
        self.ws.on_error = self.on_error
        self.ws.on_close = self.on_close

        self.ws.connect()
