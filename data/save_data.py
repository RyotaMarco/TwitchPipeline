import os
import json
from datetime import datetime
from dotenv import load_dotenv
from src.utils.log import *

load_dotenv()

logger = get_logger('save_data')

def save_all_stream_data(results, filename='streams_data.json'):

    raw_data_path = os.getenv("RAW_DATA")
    if raw_data_path is None:
        logger.error("RAW_DATA não está definida no ambiente!")
        raise 
    os.makedirs(raw_data_path, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(raw_data_path, f"streams_data_{timestamp}.json")

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    logger.info(f"Dados salvos em: {filename}")

if __name__ == "__main__":
    exemplo = {"stream_id": 123, "viewer_count": 456}
    save_all_stream_data(exemplo)