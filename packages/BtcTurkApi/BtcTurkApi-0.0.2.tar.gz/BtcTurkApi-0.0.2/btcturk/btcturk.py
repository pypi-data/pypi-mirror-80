import time, base64, hmac, hashlib, requests, json

class BtcTurk():
    BASE_URL = "https://api.btcturk.com"
    GRAPH_BASE_URL = "https://graph-api.btcturk.com"

    def __init__(self, api_key=None, api_Secret=None):
        self.api_key = api_key
        self.api_Secret = api_Secret

    def _headers(self,protection):  
        if protection:
            if self.api_key and self.api_Secret:
                apiSecret = base64.b64decode(self.api_Secret)
                stamp = str(int(time.time())*1000)
                data = "{}{}".format(self.api_key, stamp).encode("utf-8")
                signature = hmac.new(apiSecret, data, hashlib.sha256).digest()
                signature = base64.b64encode(signature) 
                return {"X-PCK": self.api_key, "X-Stamp": stamp, "X-Signature": signature, "Content-Type" : "application/json"}            
            else:
                return "You must set your public and private key for this method."
        return {}

    def ticker(self,pair_symbol = None):
        if pair_symbol:
            method = "/api/v2/ticker?pairSymbol=" + pair_symbol
            uri = self.BASE_URL + method
            result = requests.get(url=uri)
            result = result.json()
            return json.dumps(result, indent=2)
        else:
            method = "/api/v2/ticker"
            uri = self.BASE_URL + method
            result = requests.get(url=uri)
            result = result.json()
            return json.dumps(result, indent=2)

    def get_order_book(self,pair_symbol = None):
        if pair_symbol:
            method = "/api/v2/orderbook?pairSymbol=" + pair_symbol
            uri = self.BASE_URL + method
            result = requests.get(url=uri)
            result = result.json()
            return json.dumps(result, indent=2)
        else:
            return "Choose a pair Symbol for this method."
    
    def get_all_trades(self,pair_symbol = None,last = None):
        if pair_symbol:
            method = "/api/v2/trades?pairSymbol=" + pair_symbol
            uri = self.BASE_URL + method
            if last:
                uri = self.BASE_URL + method
                result = requests.get(url=uri +"&"+ last)
                result = result.json()
                return json.dumps(result, indent=2)
            else:
                uri = self.BASE_URL + method
                result = requests.get(url=uri)
                result = result.json()
                return json.dumps(result, indent=2)
        else:
            return "Choose a pair Symbol for this method."

    def get_all_ohcl(self,pair_symbol):
        if pair_symbol:
            method = "/v1/ohlcs?pair=" + pair_symbol
            uri = self.GRAPH_BASE_URL + method
            result = requests.get(url=uri)
            result = result.json()
            return json.dumps(result, indent=2)
        else:
            return "Choose a pair Symbol for this method."

    def get_balances(self):
        method = "/api/v1/users/balances"
        uri = self.BASE_URL + method
        result = requests.get(url=uri, headers=self._headers(True))
        result = result.json()
        return json.dumps(result, indent=2)

    def get_transactions(self):
        method = "/api/v1/users/transactions/trade"
        uri = self.BASE_URL + method
        result = requests.get(url=uri, headers=self._headers(True))
        result = result.json()
        return json.dumps(result, indent=2)

    def get_open_order(self,pair_symbol):    
        if pair_symbol:
            method = "/api/v1/openOrders?pairSymbol=" + pair_symbol
            uri = self.BASE_URL + method
            result = requests.get(url=uri, headers=self._headers(True))
            result = result.json()
            return json.dumps(result, indent=2)
        else:
            return "Choose a pair Symbol for this method."

    def cancel_order(self,order_id):
        if order_id:
            method = "/api/v1/order?id=" + order_id
            uri = self.BASE_URL + method
            result = requests.get(url=uri, headers=self._headers(True))
            result = result.json()
            return json.dumps(result, indent=2)
        else:
            return "Choose a pair Symbol for this method."
    
    def market_sell(self, pair_symbol, quantity):
        method = "/api/v1/order"
        uri = self.BASE_URL + method
        params={"quantity": quantity ,"price": "0","stopPrice": 0, "newOrderClientId":"BtcTurk API", "orderMethod":"market", "orderType":"sell", "pairSymbol":pair_symbol}
        result = requests.post(url=uri, headers=self._headers(True), json=params)
        result = result.json()
        return json.dumps(result, indent=2)

    def market_buy(self, pair_symbol, quantity):
        method = "/api/v1/order"
        uri = self.BASE_URL + method
        params={"quantity": quantity ,"price": "0","stopPrice": 0, "newOrderClientId":"BtcTurk API", "orderMethod":"market", "orderType":"buy", "pairSymbol":pair_symbol}
        result = requests.post(url=uri, headers=self._headers(True), json=params)
        result = result.json()
        return json.dumps(result, indent=2)

    def limit_sell(self, pair_symbol, quantity, price):
        method = "/api/v1/order"
        uri = self.BASE_URL + method
        params={"quantity": quantity ,"price": price,"stopPrice": 0, "newOrderClientId":"BtcTurk API", "orderMethod":"limit", "orderType":"sell", "pairSymbol":pair_symbol}
        result = requests.post(url=uri, headers=self._headers(True), json=params)
        result = result.json()
        return json.dumps(result, indent=2)

    def limit_buy(self, pair_symbol, quantity, price):
        method = "/api/v1/order"
        uri = self.BASE_URL + method
        params={"quantity": quantity ,"price": price,"stopPrice": 0, "newOrderClientId":"BtcTurk API", "orderMethod":"limit", "orderType":"buy", "pairSymbol":pair_symbol}
        result = requests.post(url=uri, headers=self._headers(True), json=params)
        result = result.json()
        return json.dumps(result, indent=2)

    def stop_sell(self, pair_symbol, quantity, price, stop_price):
        method = "/api/v1/order"
        uri = self.BASE_URL + method
        params={"quantity": quantity ,"price": price,"stopPrice": stop_price, "newOrderClientId":"BtcTurk API", "orderMethod":"stoplimit", "orderType":"sell", "pairSymbol":pair_symbol}
        result = requests.post(url=uri, headers=self._headers(True), json=params)
        result = result.json()
        return json.dumps(result, indent=2)

    def stop_buy(self, pair_symbol, quantity, price, stop_price):
        method = "/api/v1/order"
        uri = self.BASE_URL + method
        params={"quantity": quantity ,"price": price,"stopPrice": stop_price, "newOrderClientId":"BtcTurk API", "orderMethod":"stoplimit", "orderType":"buy", "pairSymbol":pair_symbol}
        result = requests.post(url=uri, headers=self._headers(True), json=params)
        result = result.json()
        return json.dumps(result, indent=2)



    

