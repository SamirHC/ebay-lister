import item_lister, logger
import time

if __name__ == "__main__":
    start_time = time.time()

    item_lister.write_items_to_csv()

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.log_response(f"Total elapsed time: {elapsed_time:.4f} seconds")
