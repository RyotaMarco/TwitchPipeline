from config.twitch_config import get_headers
import requests

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

