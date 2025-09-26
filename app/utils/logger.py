import logging
from pathlib import Path

from app.utils import time_util
from app.utils.dirs import LOG_DIR


def get_log_file_name() -> Path:
    file_name = f"{time_util.get_timestamp()}.txt"
    return LOG_DIR / file_name


def setup_logging():
    logging.basicConfig(
        filename=get_log_file_name(),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def log_response(response: str):
    logging.info(response)
    print(response)
