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
            self.logger.debug(f"Fazendo requisição para: {url} com params: {params}")
            response = requests.get(url, headers=headers, params=params)

            remaining = int(response.headers.get("Ratelimit-Remaining", 800))
            reset_time = int(response.headers.get("Ratelimit-Reset", 0))
            
            if remaining <= 10:
                current_time = int(time.time())
                wait_time = reset_time - current_time
                if wait_time > 2:
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
        
        self.logger.info("Buscando streams ao vivo da Twitch...")
        streams = self.handle_pagination(url, headers, params)
        self.logger.info(f"Total de streams obtidos: {len(streams)}")
        
        return streams


    def filter_stream_data(self, stream):
        '''
        Process a single stream data locally without making additional API calls.
        '''
        try:

            filtered_data = {
                'user_id': stream['user_id'],
                'user_name': stream['user_name'],
                'stream_id': stream['id'],
                'viewer_count': stream['viewer_count'],
                'game_name': stream['game_name'],
                'started_at': stream['started_at'],
                'is_mature': stream['is_mature'],
                'thumbnail_url': stream['thumbnail_url']
            }
        
            
            return filtered_data
        except KeyError as e:
            self.logger.error(f"Campo ausente nos dados do stream: {e}")
            return {'stream_id': stream.get('id', 'unknown'), 'error': f'Campo ausente: {e}'}
        except Exception as e:
            self.logger.error(f"Erro ao processar dados do stream: {e}")
            return {'stream_id': stream.get('id', 'unknown'), 'error': str(e)}


    def process_streams_data(self, streams):
        '''
        Process all streams data without additional API calls
        '''
        processed_streams = []
        
        for i, stream in enumerate(streams):
            if i % 10000 == 0:
                self.logger.debug(f"Processando stream {i+100}/{len(streams)}")
                
            filtered_data = self.filter_stream_data(stream)
            if 'error' not in filtered_data:
                processed_streams.append(filtered_data)
            else:
                self.logger.warning(f"Stream descartado devido a erro: {filtered_data}")
        
        self.logger.info(f"Processados {len(processed_streams)} streams com sucesso")
        return processed_streams
    
    