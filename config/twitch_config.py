import requests     
import dotenv
import os

dotenv.load_dotenv()

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
acess_token = token_data["access_token"]

headers = {
    'Authorization': f"Bearer {acess_token}",
    'Client-Id': id_client
}
r = requests.get('https://api.twitch.tv/helix/streams/', headers=headers)
r.raise_for_status()
print(r.json())


