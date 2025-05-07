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

def save_parquet_stream_data(df_results, filename='streams_data.parquet', partition_col=None):
    processed_data_path = os.getenv("PROCESSED_DATA")
    if processed_data_path is None:
        logger.error("PROCESSED_DATA não está definida no ambiente!")
        raise ValueError("PROCESSED_DATA não está definida no ambiente!")
    os.makedirs(processed_data_path, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(processed_data_path, f"streams_data_{timestamp}")

    
    writer = df_results.write.mode("overwrite")
    if partition_col:
        writer = writer.partitionBy(partition_col)
    writer.parquet(output_path)

    logger.info(f"Dados salvos em formato Parquet: {output_path}")
    return output_path
        

if __name__ == "__main__":
    exemplo = {"stream_id": 123, "viewer_count": 456}
    save_all_stream_data(exemplo)