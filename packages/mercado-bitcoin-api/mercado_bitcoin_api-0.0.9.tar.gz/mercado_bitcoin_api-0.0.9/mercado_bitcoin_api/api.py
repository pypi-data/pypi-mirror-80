import requests

class API:
    HOST = "www.mercadobitcoin.net"
    
    # "https://www.mercadobitcoin.net/api/<coin>/<method>/"
    URL_QUERY_PATTERN = "https://{host}/api/{coin}/{method}"
    
    def __init__(self):
        pass
    
    def _query_url(self, method, coin):
        return self.URL_QUERY_PATTERN.format(host=self.HOST, coin=coin, method=method)
    
    def raw_query(self, method, coin="BTC"):
        url = self._query_url(method, coin)
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            raise ConnectionError("Status code unexpected")
    
    def get_ticker(self, coin="BTC"):
        return self.raw_query("ticker", coin).json()
    
    def get_orderbook(self, coin="BTC"):
        return self.raw_query("orderbook", coin).json()
    
    def get_trades(self, coin="BTC"):
        return self.raw_query("trades", coin).json()
