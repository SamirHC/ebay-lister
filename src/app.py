import item_lister, logger
import time

if __name__ == "__main__":
    logger.log_response("="*80)
    logger.log_response("Starting Listing Tool...")
    logger.log_response("")
    start_time = time.time()

    item_lister.main()

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.log_response(f"Total elapsed time: {elapsed_time:.4f} seconds.")
