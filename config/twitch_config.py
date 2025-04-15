import requests     
import dotenv
import os

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


    response = requests.post(token_url, params=params)
    response.raise_for_status()
    token_data = response.json()
    return token_data["access_token"]

def get_headers():
    acess_token = get_acess_token()

    id_client = os.getenv("ID_CLIENT")

    return {
        'Authorization': f"Bearer {acess_token}",
        'Client-Id': id_client
    }


