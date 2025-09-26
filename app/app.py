import time

from app import item_lister
from app.utils import logger


def run():
    logger.log_response("="*80)
    logger.log_response("Starting Listing Tool...")
    logger.log_response("")
    start_time = time.perf_counter()

    item_lister.main()

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    logger.log_response(f"Total elapsed time: {elapsed_time:.4f} seconds.")
