import os
import requests
import json

API_KEY = os.getenv('COINGECKO_API_KEY')
BASE_URL = 'https://pro-api.coingecko.com/api/v3/'

def fetch_coins_with_platforms():
    url = f"{BASE_URL}coins/list?include_platform=true"
    headers = {'X-Cg-Pro-Api-Key': API_KEY}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

def reorganize_by_platform(coins_with_platforms):
    platforms_with_coins = {}
    for coin in coins_with_platforms:
        for platform, address in coin['platforms'].items():
            if platform not in platforms_with_coins:
                platforms_with_coins[platform] = []
            platforms_with_coins[platform].append(coin['id'])
    return platforms_with_coins

def save_platforms_with_coins(platforms_with_coins):
    with open('platforms_with_coins.json', 'w') as f:
        json.dump(platforms_with_coins, f, indent=2)

if __name__ == '__main__':
    coins_with_platforms = fetch_coins_with_platforms()
    platforms_with_coins = reorganize_by_platform(coins_with_platforms)
    save_platforms_with_coins(platforms_with_coins)