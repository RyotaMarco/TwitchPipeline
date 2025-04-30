from src.api.twitch_api import get_streams


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