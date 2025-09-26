import time

from app import item_lister
from app.utils import logger


def run(parallel=True):
    csv_line_getter = item_lister.get_csv_lines_parallel if parallel else item_lister.get_csv_lines

    logger.log_response("="*80)
    logger.log_response("Starting Listing Tool...")
    logger.log_response("")

    start_time = time.perf_counter()

    logger.log_response("Started uploading images.")
    image_urls = item_lister.get_image_urls()
    logger.log_response("Finished uploading images.\n")
    lines = csv_line_getter(image_urls)
    item_lister.write_items_to_csv(lines)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    logger.log_response(f"Total elapsed time: {elapsed_time:.4f} seconds.")
