import requests     
import dotenv
import os
from requests.exceptions import HTTPError
import time
import random

dotenv.load_dotenv()
'''
Main configuration for using the Twitch API
'''

def get_acess_token():
    id_client = os.getenv("ID_CLIENT")
    secret_client = os.getenv("SECRET_CLIENT")
    token_url = os.getenv("TOKEN_URL")


    params = {
        'client_id': id_client,
        'client_secret': secret_client,
        'grant_type': 'client_credentials'
    }

    max_retries=5
    for attempt in range(max_retries):
        try:
            response = requests.post(token_url, params=params)
            response.raise_for_status()
            token_data = response.json()
            return token_data["access_token"]
        except HTTPError as e:
            if e.response.status_code == 502 or 500:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Erro 502 ao obter token. Tentativa {attempt+1}/{max_retries}. Aguardando {wait_time:.2f}s...")
                time.sleep(wait_time)
                continue
            else:
                raise

def get_headers():
    acess_token = get_acess_token()

    id_client = os.getenv("ID_CLIENT")

    return {
        'Authorization': f"Bearer {acess_token}",
        'Client-Id': id_client
    }


