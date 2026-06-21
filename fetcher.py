import requests
import pandas as pd

def get_data_live(symbol:str=None, interval:str="1m", limit:int=1):
    if symbol is None or interval is None:
        raise ValueError("Symbol and interval must be provided.")
    
    PARAMS = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get("http://binance.com/api/v3/klines", params=PARAMS).json()
    latest_rcord = pd.DataFrame(response, columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"])
    latest_rcord['symbol'] = symbol
    return latest_rcord
