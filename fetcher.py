import requests

PARAMS = {
    "symbol": "BTCUSDT",
    "interval": "1m",
    "limit": 1
}

response = requests.get("http://binance.com/api/v3/klines", params=PARAMS).json()
print(response)