import os
import json
from datetime import datetime


def save_all_stream_data(results, filename='streams_data.json'):

    os.makedirs(os.getenv("RAW_DATA"), exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(os.getenv("RAW_DATA"), f"streams_data_{timestamp}.json")

    with open (filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Dados salvos em: {filename}")