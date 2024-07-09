import item_lister
import time

if __name__ == "__main__":
    start_time = time.time()

    item_lister.write_items_to_csv()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total elapsed time: {elapsed_time:.4f} seconds")
