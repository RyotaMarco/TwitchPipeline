from config.twitch_config import get_headers
import time
import os
import requests
from typing import List, Dict
from src.utils.log import *




class TwitchAPI:
    '''
    Access the Twitch API with the correct parameters for this project
    '''
    def __init__(self):
            self.logger = get_logger("twitch_api_request")
            self.base_url = os.getenv("BASE_URL")


    def request_with_rate_limit(self, url, headers, params):
        '''
        request API with limit handler
        '''

        try:

            response = requests.get(url, headers=headers, params=params)


            remaining = int(response.headers.get("Ratelimit-Remaining", 800))
            reset_time = int(response.headers.get("Ratelimit-Reset", 0))
            

            if remaining <= 3:
                current_time = int(time.time())
                wait_time = reset_time - current_time
                if wait_time > 0:
                    self.logger.warning(f"Aguardando {wait_time} segundos.")
                    time.sleep(wait_time)


            response.raise_for_status()
            return response



        except Exception as e:
            self.logger.error(f"Erro na requisição: {e}")
            raise




    def fetch_page(self, url, headers, params):
        '''
        Convert response request to JSON
        '''
        response = self.request_with_rate_limit(url, headers, params)
        return response.json()



    def handle_pagination(self, initial_url, headers, params):
        '''
        Handle pagination in cursor, to request all of them
        '''

        pagination_results = []
        cursor = None

        while True:
            current_params = params.copy()
            if cursor:
                current_params['after'] = cursor


            data = self.fetch_page(initial_url, headers, current_params)
            pagination_results.extend(data['data'])

            cursor = data.get('pagination', {}).get('cursor')
            if not cursor:
                break
        
        return pagination_results



    def get_streams(self):
        '''
        get streams, principal method
        '''
        
        url = f"{self.base_url}/streams"
        headers = get_headers()


        params = {
            'type': 'live',
            'first': '100',
        }

        return self.handle_pagination(url, headers, params)



    def get_filtered_params(self, stream_id):
        '''obtain stream info with ID '''

        url = f"{self.base_url}/streams"
        headers = get_headers()

        params = {
            'user_id': stream_id
        }

        try:
            response_data = self.fetch_page(url, headers, params)
            

            data = response_data.get('data', [])
        
            if data:
                filtered_data = data[0]
                return {
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
            

        except Exception as e:
            self.logger.error(f"Erro ao obter informações do stream {stream_id}: {e}")
            raise        
