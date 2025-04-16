import time
from config.twitch_config import get_headers
import requests

'''
Access the Twitch API with the correct parameters for this project
'''


BASE_URL = 'https://api.twitch.tv/helix'

def get_streams():
    
    url = f"{BASE_URL}/streams?"
    cursor = None




    headers = get_headers()

    results_api = []

    while True:

        params = {
            'type': 'live',
            'first': '100',
        }

        if cursor:
            params['after'] = cursor
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        response_json = response.json()
        cursor = response_json.get('pagination', {}).get('cursor')
        results_api.extend(response_json['data'])
        if not cursor:
            break
        
        time.sleep(0.5)
    return results_api



def get_filtered_params(data):


    filtered_json= {
    'data_fill': [
            {
                'user_id':filtered_data['user_id'],
                'user_name':filtered_data['user_name'],
                'Stream_id':filtered_data['id'],
                'viewer_count':filtered_data['viewer_count'],
                'game_name':filtered_data['game_name'],
                'started_at':filtered_data['started_at'],
                'is_mature':filtered_data['is_mature'],
                'thumbnail_url':filtered_data['thumbnail_url']
            }
            for filtered_data in data
        ]
    }    
    return filtered_json

def get_viewers_by_category():
    twitch_request = get_streams()

    category_viewers = {}
    for stream in twitch_request['data']:
        category = stream['game_name']
        viewers = stream['viewer_count']

        if category in category_viewers:
            category_viewers[category] += viewers
        
        else:
            category_viewers[category] = viewers

    return category_viewers
    