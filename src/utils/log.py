import logging
import os
from datetime import datetime


def log_config():
    log_path_file = os.getenv("LOG_FILE_PATH")

    if log_path_file is None:
        raise ValueError("LOG_FILE_PATH não está definido no ambiente!")
    os.makedirs(log_path_file, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(log_path_file, f"log_file_{timestamp}.log")

    logging.basicConfig(filename= filename, encoding='utf-8', level= logging.DEBUG)
