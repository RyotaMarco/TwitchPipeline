
from config.twitch_config import get_headers
import time
import os
import requests
from typing import List, Dict
from utils.log import *

'''
Access the Twitch API with the correct parameters for this project
'''
logger = get_logger("Twitch_api_request")

BASE_URL = os.getenv("BASE_URL")

def get_streams():
    
    url = f"{BASE_URL}/streams?"
    cursor = None
    headers = get_headers()
    total_id = []


    while True:

        params = {
            'type': 'live',
            'first': '100',
        }


        if cursor:
            params['after'] = cursor

        response = requests.get(url, headers=headers, params=params)
        limit = int(response.headers.get("Ratelimit-Limit", 800))
        remaining = int(response.headers.get("Ratelimit-Remaining", 800))
        reset_time = int(response.headers.get("Ratelimit-Reset", 0))
        

        response.raise_for_status()
        response_json = response.json()


        streams_id = [item['user_id'] for item in response_json.get('data', [])] #get Ids
        total_id.extend(streams_id)

        # Verify pagination
        cursor = response_json.get('pagination',{}).get('cursor')

        # rate limit 
        if remaining <= 3:
            current_time = int(time.time())
            wait_time = reset_time - current_time
            if wait_time > 0:
                logger.warning(f"Aguardando {wait_time} segundos.")
                time.sleep(wait_time)

        if not cursor:
            break

    return total_id



def get_filtered_params(stream_id):
    '''obtain stream info with ID '''

    url = f"{BASE_URL}/streams?user_id={stream_id}"
    headers = get_headers()


    response = requests.get(url, headers=headers)

    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {response.json()}")
    logger.info(f"Headers: {response.headers}")


    data = response.json().get('data', [])

    limit = int(response.headers.get("Ratelimit-Limit", 800))
    remaining = int(response.headers.get("Ratelimit-Remaining", 800))
    reset_time = int(response.headers.get("Ratelimit-Reset", 0))


    

    


    if remaining <= 5:
        current_time = int(time.time())
        wait_time = reset_time - current_time
        if wait_time > 0:
            logger.info(f"Aguardando {wait_time} segundos.")
            time.sleep(wait_time)
    
    if data:
        filtered_data = data[0]
        return{
        'user_id':filtered_data['user_id'],
        'user_name':filtered_data['user_name'],
        'Stream_id':filtered_data['id'],
        'viewer_count':filtered_data['viewer_count'],
        'game_name':filtered_data['game_name'],
        'started_at':filtered_data['started_at'],
        'is_mature':filtered_data['is_mature'],
        'thumbnail_url':filtered_data['thumbnail_url']
        }    
    else:
        return {'stream_id': stream_id, 'error': 'Stream não encontrado'}
    