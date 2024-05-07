import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# Get the API key from an environment variable
API_KEY = os.getenv('COINGECKO_API_KEY')
BASE_URL = 'https://pro-api.coingecko.com/api/v3'

# Check if the API_KEY is correctly set in your environment variables
if API_KEY is None:
    raise ValueError("COINGECKO_API_KEY environment variable not set")

def load_selected_coins(csv_path='selected_coins.csv'):
    """Load selected coin IDs from a CSV file."""
    return pd.read_csv(csv_path)['id'].tolist()

def fetch_historical_data(coin_id, start_date, end_date):
    """Fetch historical price and market cap data for a single cryptocurrency."""
    url = f"{BASE_URL}/coins/{coin_id}/market_chart/range"
    headers = {'X-Cg-Pro-Api-Key': API_KEY}
    params = {
        'vs_currency': 'usd',
        # Adjust start date to one day earlier to ensure coverage
        'from': (start_date - timedelta(days=2)).timestamp(),
        'to': end_date.timestamp()
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        df['market_cap'] = pd.DataFrame(data['market_caps'], columns=['timestamp', 'market_cap'])['market_cap']
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df['coin_id'] = coin_id
        # Filter the DataFrame to the original date range
        return df[start_date:end_date]
    else:
        print(f"Failed to fetch data for {coin_id}: {response.text}")
        return pd.DataFrame()

# Load selected coins
coin_ids = load_selected_coins()

# Define your date range
start_date = datetime(2021, 1, 1)
end_date = datetime(2023, 12, 31)

# Collect all data
all_data = pd.DataFrame()

for coin_id in coin_ids:
    df = fetch_historical_data(coin_id, start_date - timedelta(days=1), end_date)
    all_data = pd.concat([all_data, df], ignore_index=False)

# Save the data to CSV
all_data.reset_index().to_csv('crypto_data.csv', index=False)
