import os
from datetime import datetime
import logging


def get_logger(name=__name__):
    log_path_file = os.getenv("LOG_FILE_PATH")
    if log_path_file is None:
        raise ValueError("LOG_FILE_PATH não está definido no ambiente!")
    os.makedirs(log_path_file, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_path_file, f"log_file_{timestamp}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
