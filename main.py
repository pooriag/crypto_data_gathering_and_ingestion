import time
import logging
import sys

import pandas as pd

import fetcher
import data_ingestion

RECOVERY_FILE = "buffer_recovery.jsonl"
SYMBOLS = ["BTCUSDT", "ETHUSDT"]

def setup_logger(name:str = "crypto_pipeline") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    log_formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d -> %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_formatter)

    file_handler = logging.FileHandler("execution_info.log", mode="a")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

def load_recovery_file():
    recovered_data = []
    if os.path.exists(RECOVERY_FILE):
        with open(RECOVERY_FILE, "r") as f:

if __name__ == "__main__":
    buffer = []
    while(True):
        
        for symbol in symbols:
            PARAMS = {
                "symbol": symbol,
                "interval": "1m",
                "limit": 1
            }
            latest_data = fetcher.get_data_live(**PARAMS)
            buffer.append(latest_data)

            print(latest_data.iloc[-1])

            if len(buffer) >= 10:
                concated_records = pd.concat(buffer, ignore_index=True)
                data_ingestion.ingest_data_to_db()
                buffer = []

        time.sleep(60)