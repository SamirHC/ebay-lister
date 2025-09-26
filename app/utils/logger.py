import logging
import os

from app.utils import time_util


LOG_DIR = os.path.join("out", "log")


def get_log_file_name():
    file_name = f"{time_util.get_timestamp()}.txt"
    return os.path.join(LOG_DIR, file_name)


logging.basicConfig(
    filename=get_log_file_name(),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_response(response):
    logging.info(response)
    print(response)
