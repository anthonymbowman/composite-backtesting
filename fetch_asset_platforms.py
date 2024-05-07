import os
import requests
import json

API_KEY = os.getenv('COINGECKO_API_KEY')
BASE_URL = 'https://pro-api.coingecko.com/api/v3/'

def fetch_asset_platforms():
    url = f"{BASE_URL}asset_platforms"
    headers = {'X-Cg-Pro-Api-Key': API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch asset platforms: {response.status_code}")

if __name__ == '__main__':
    asset_platforms = fetch_asset_platforms()
    with open('asset_platforms.json', 'w') as f:
        json.dump(asset_platforms, f)
