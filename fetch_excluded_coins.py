import os
import requests
import json

API_KEY = os.getenv('COINGECKO_API_KEY')
BASE_URL = 'https://pro-api.coingecko.com/api/v3/'

EXCLUDE_CATEGORY_IDS = [
    'aave-tokens', 'compound-tokens', 'ctokens', 'defi-index', 'eth-2-0-staking', 
    'leveraged-token', 'liquid-restaking-tokens', 'liquid-staking-tokens', 
    'lp-tokens', 'mirrored-assets', 'nft-index', 
    'rebase-tokens', 'stablecoins', 'structured-products', 
    'synths', 'tokenized-btc', 'tokenized-commodities',
    'tokenized-products', 'tokensets', 'wormhole-assets', 'wrapped-tokens', 
    'yearn-vault-tokens'
]

def get_coins_by_category(category_id):
    coins = []
    page = 1
    has_more = True
    while has_more:
        url = f"{BASE_URL}coins/markets?vs_currency=usd&category={category_id}&page={page}"
        headers = {'X-Cg-Pro-Api-Key': API_KEY}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            page_data = response.json()
            if not page_data:
                has_more = False  # No more data to fetch
            else:
                coins.extend(page_data)
                page += 1
        else:
            has_more = False
    return coins

def fetch_excluded_coins():
    excluded_coins = []
    for category_id in EXCLUDE_CATEGORY_IDS:
        excluded_coins.extend(get_coins_by_category(category_id))
    return {coin['id'] for coin in excluded_coins}  # Set of unique coin IDs

if __name__ == '__main__':
    excluded_coin_ids = fetch_excluded_coins()
    # Write the list of excluded coin IDs to a file
    with open('excluded_coin_ids.json', 'w') as f:
        json.dump(list(excluded_coin_ids), f)
