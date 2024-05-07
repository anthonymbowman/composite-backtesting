from datetime import datetime
import os
import requests
import streamlit as st
import json
import base64
from fetch_data import fetch_data_for_coins
from backtest import perform_backtest

API_KEY = os.getenv('COINGECKO_API_KEY')
BASE_URL = 'https://pro-api.coingecko.com/api/v3/'

def load_excluded_coin_ids():
    try:
        with open('excluded_coin_ids.json', 'r') as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        st.error(f'excluded_coin_ids.json file not found or contains invalid JSON. Error: {e}')
        return set()  # Return an empty set if there's an error

def load_platforms_with_coins():
    try:
        with open('platforms_with_coins.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error('platforms_with_coins.json file not found. Please run fetch_tokens_with_chains.py to generate it.')
        return {}

# Define the load_asset_platforms function
def load_platform_details():
    try:
        with open('asset_platforms.json', 'r') as f:
            platforms_data = json.load(f)
            platform_options = {platform['id']: platform['name'] for platform in platforms_data}
            return platform_options
    except FileNotFoundError:
        st.error('asset_platforms.json file not found. Please ensure the file is generated and available.')
        return {}

def get_categories():
    url = f"{BASE_URL}coins/categories/list"
    headers = {'X-Cg-Pro-Api-Key': API_KEY}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else []

def get_coins_by_category(category_id, min_market_cap):
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
                has_more = False
            else:
                for coin in page_data:
                    if coin['ath'] is not None and coin['total_supply'] is not None:
                        market_cap_estimate = coin['ath'] * coin['total_supply']
                        if market_cap_estimate >= min_market_cap:
                            coins.append({'id': coin['id'], 'name': coin['name'], 'symbol': coin['symbol'].upper(), 'market_cap': coin['market_cap']})
                page += 1
        else:
            has_more = False
    return coins

def app():
    st.title("Crypto Backtesting Tool")
    st.header("Filter Coins for Backtesting")
    # Load necessary data
    platform_options = load_platform_details()
    platforms_with_coins = load_platforms_with_coins()
    excluded_coin_ids = load_excluded_coin_ids()
    min_market_cap = st.number_input("Minimum Market Cap", min_value=0, value=100000000, step=1000000)
    default_platform_name = platform_options.get('ethereum', 'Ethereum')
    selected_platform_names = st.multiselect(
        "Select Asset Platforms", options=list(platform_options.values()), default=[default_platform_name]
    )
    name_to_id = {name: id for id, name in platform_options.items()}
    selected_platform_ids = [name_to_id[name] for name in selected_platform_names if name in name_to_id]
    categories = get_categories()
    category_options = {cat['name']: cat['category_id'] for cat in categories}
    selected_categories = st.multiselect("Select Categories to Include", options=list(category_options.keys()))
    excluded_categories = st.multiselect("Select Categories to Exclude", options=list(category_options.keys()))
    selected_category_ids = [category_options[cat] for cat in selected_categories if cat in category_options]
    excluded_category_ids = [category_options[cat] for cat in excluded_categories if cat in category_options]

    # Fetch coins for included categories
    included_coins = []
    if selected_category_ids:
        for category_id in selected_category_ids:
            included_coins.extend(get_coins_by_category(category_id, min_market_cap))

    # Fetch coins for excluded categories
    excluded_coins = []
    if excluded_category_ids:
        for category_id in excluded_category_ids:
            excluded_coins.extend(get_coins_by_category(category_id, min_market_cap))

    # Remove duplicates and filter by platform
    included_coins_dict = {coin['id']: coin for coin in included_coins}
    excluded_coin_ids_set = set(excluded_coin_ids)
    excluded_coins_dict = {coin['id']: coin for coin in excluded_coins}

    # Exclude coins based on excluded categories and IDs
    final_coin_ids = set(included_coins_dict.keys()) - set(excluded_coins_dict.keys()) - excluded_coin_ids_set

    # Filter coins based on selected platforms
    coins_on_selected_platforms = set()
    for platform_id in selected_platform_ids:
        coins_on_selected_platforms.update(platforms_with_coins.get(platform_id, []))

    final_coins = [included_coins_dict[coin_id] for coin_id in final_coin_ids if coin_id in coins_on_selected_platforms]

    # Sort coins by market cap
    final_coins = sorted(final_coins, key=lambda x: x['market_cap'] if x['market_cap'] is not None else 0, reverse=True)

    with st.expander("Exclude Specific Coins"):
    # User interaction for coin selection with formatted display
        st.write("Select Coins to Include in the Backtest:")
        for coin in final_coins:
            coin_label = f"{coin['name']} ({coin['symbol']})"
            if st.checkbox(coin_label, value=True, key=coin['id']):
                # This is where you handle user selection, possibly storing the selected coins
                pass
    
    selected_coin_ids = [coin['id'] for coin in final_coins if st.session_state.get(coin['id'], True)]

    st.header("Backtesting Configuration")
    # Parameters
    start_date = st.date_input("Start Date", value=datetime(2021, 1, 1))
    end_date = st.date_input("End Date", value=datetime(2023, 12, 31))
    weighting_scheme = st.selectbox("Weighting Scheme", ['Equal', 'Capped-25', 'Proportional', 'Square Root'])
    max_number_of_components = st.number_input("Maximum Number of Components", min_value=1, value=10)
    rebalance_frequency = st.selectbox("Rebalance Frequency", ['Daily', 'Monthly', 'Quarterly'])

    if st.button("Run Backtest"):
        st.write(f"{len(selected_coin_ids)} coins selected for backtesting.")
        historical_data = fetch_data_for_coins(selected_coin_ids, start_date, end_date)
        csv = historical_data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="historical_data.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)
        # st.dataframe(historical_data)
        if not historical_data.empty:
            backtest_results = perform_backtest(historical_data, start_date, end_date, weighting_scheme, max_number_of_components, rebalance_frequency)
            st.line_chart(backtest_results['portfolio_value'])
        else:
            st.error("Failed to fetch historical data.")
        # Add a download link for the backtest results
        csv = backtest_results.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="backtest_results.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)
        

if __name__ == "__main__":
    app()
