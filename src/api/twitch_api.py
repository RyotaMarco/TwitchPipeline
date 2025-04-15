from config.twitch_config import get_headers
import requests

'''
Access the Twitch API with the correct parameters for this project
'''


BASE_URL = 'https://api.twitch.tv/helix'

def get_streams(user_login=None,  game_id=None):
    url = f"{BASE_URL}/streams"

    params = {
        'type': 'live',
        'first': '100'
    }

    headers = get_headers()

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

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

def get_filtered_params():
    twitch_request = get_streams()

    filtered_json= {
    'data_fill': [
            {
                'user_id':data['user_id'],
                'user_name':data['user_name'],
                'Stream_id':data['id'],
                'viewer_count':data['viewer_count'],
                'game_name':data['game_name'],
                'started_at':data['started_at'],
                'is_mature':data['is_mature'],
                'thumbnail_url':data['thumbnail_url']
            }
            for data in twitch_request['data']
        ]
    }    
    return filtered_json
    