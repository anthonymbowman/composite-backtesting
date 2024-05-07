import os
import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = os.getenv('COINGECKO_API_KEY')
BASE_URL = 'https://pro-api.coingecko.com/api/v3'

if API_KEY is None:
    raise ValueError("COINGECKO_API_KEY environment variable not set")

def fetch_historical_data(coin_id, start_date, end_date):
    """Fetch historical price and market cap data for a single cryptocurrency."""
    url = f"{BASE_URL}/coins/{coin_id}/market_chart/range"
    headers = {'X-Cg-Pro-Api-Key': API_KEY}
    params = {
        'vs_currency': 'usd',
        'from': (datetime.combine(start_date, datetime.min.time()) - timedelta(days=2)).timestamp(),
        'to': datetime.combine(end_date, datetime.min.time()).timestamp()
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        df['market_cap'] = pd.DataFrame(data['market_caps'], columns=['timestamp', 'market_cap'])['market_cap']
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df['coin_id'] = coin_id
        return df.reset_index()  # Ensure 'timestamp' is a column after resetting the index
    else:
        print(f"Failed to fetch data for {coin_id}: {response.text}")
        return pd.DataFrame()

def fetch_data_for_coins(coin_ids, start_date, end_date):
    """Fetch historical data for a list of coins."""
    all_data = pd.DataFrame()
    for coin_id in coin_ids:
        df = fetch_historical_data(coin_id, start_date, end_date)
        all_data = pd.concat([all_data, df], ignore_index=False)
    return all_data

