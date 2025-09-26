import logging
import os
from datetime import datetime


LOG_DIR = os.path.join("out", "log")


def get_log_file_name():
    time_str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    return os.path.join(LOG_DIR, f"{time_str}.txt")


logging.basicConfig(
    filename=get_log_file_name(),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_response(response):
    logging.info(response)
    print(response)
