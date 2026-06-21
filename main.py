import time
import pandas as pd

import fetcher
import data_ingestion

if __name__ == "__main__":
    buffer = None
    while(True):
        symbols = ["BTCUSDT", "ETHUSDT"]
        for symbol in symbols:
            PARAMS = {
                "symbol": symbol,
                "interval": "1m",
                "limit": 1
            }
            latest_data = fetcher.get_data_live(**PARAMS)
            if buffer is None:
                buffer = latest_data
            else: buffer = pd.concat([buffer, latest_data], ignore_index=True)

            time.sleep(60)
            print(latest_data.iloc[-1])

            if len(buffer) > 60:
                data_ingestion.ingest_data_to_db(buffer)
                buffer = None