from config import twitch_config
import requests

r = requests.get('https://api.twitch.tv/helix/streams/', headers=twitch_config.headers)
r.raise_for_status()
print(r.json())

token_info = r.json()
print(token_info)
