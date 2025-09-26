import time

from app import csv_builder
from app.utils import dirs
from app.utils import logger


def run():
    dirs.setup_directories()
    logger.setup_logging()

    logger.log_response("="*80)
    logger.log_response("Starting Listing Tool...")
    logger.log_response("")

    start_time = time.perf_counter()

    logger.log_response("Started uploading images.")
    image_urls = csv_builder.get_image_urls()
    logger.log_response("Finished uploading images.\n")
    ebay_items = csv_builder.get_ebay_items(image_urls)
    csv_builder.write_items_to_csv(ebay_items)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    logger.log_response(f"Total elapsed time: {elapsed_time:.4f} seconds.")
