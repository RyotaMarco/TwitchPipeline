from src.api.twitch_api import *

'''print(get_streams())

print(get_filtered_params())'''

data_api = get_streams()

print(get_filtered_params(data_api))