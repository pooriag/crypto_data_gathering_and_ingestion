import time
import logging
import sys
import os
import json

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
        logger.info(f"Recovery file {RECOVERY_FILE} found. Loading data...")
        with open(RECOVERY_FILE, "r") as f:
            for line in f:
                recovered_data.append(pd.DataFrame([json.loads(line)]))
        logger.info(f"Loaded {len(recovered_data)} records from recovery file.")

    return recovered_data

def clear_recovery_file():
    if os.path.exists(RECOVERY_FILE):
        with open(RECOVERY_FILE, "w") as f:
            f.truncate(0)
            logger.debug(f"Cleared recovery file: {RECOVERY_FILE}")


def append_to_recovery_file(data):
    with open(RECOVERY_FILE, "a") as f:
        data.to_json(f, orient="records", lines=True)
        logger.debug(f"Appended a record to recovery file: {data.to_dict(orient='records')}")

if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Starting the crypto data pipeline...")

    buffer = []

    recovered_data = load_recovery_file()

    if len(recovered_data) > 0:
        buffer = recovered_data

    
    while(True):
        
        for symbol in SYMBOLS:
            PARAMS = {
                "symbol": symbol,
                "interval": "1m",
                "limit": 1
            }

            try:
                latest_data = fetcher.get_data_live(**PARAMS)
            except Exception as e:
                logger.error(f"Error occurred while fetching live data for {symbol}: {e}")
                continue

            buffer.append(latest_data)

            append_to_recovery_file(latest_data)

            logger.debug(f"Fetched data for {symbol}: {latest_data}")

            if len(buffer) >= 10:
                concated_records = pd.concat(buffer, ignore_index=True)
                data_ingestion.ingest_data_to_db()
                buffer = []
                clear_recovery_file()

        time.sleep(3)