import logging


logging.basicConfig(
    filename="log.txt",
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def log_response(response):
    logging.info(response)
    print(response)
