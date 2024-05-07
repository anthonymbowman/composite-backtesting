import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def run_backtest(df, weighting_scheme, max_number_of_components, minimum_market_cap, rebalance_frequency, start_date=datetime(2021, 1, 1), end_date=datetime(2023, 12, 31)):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by=['timestamp', 'coin_id'], inplace=True)

    initial_portfolio_value = 100
    portfolio_value = initial_portfolio_value
    current_composition = []

    freq_map = {'Daily': 'D', 'Monthly': 'MS', 'Quarterly': 'QS-JAN'}
    rebalance_dates = pd.date_range(start=start_date, end=end_date, freq=freq_map[rebalance_frequency])

    def apply_weighting_scheme(assets, scheme):
        if scheme == 'Equal':
            weights = np.ones(len(assets)) / len(assets)
        elif scheme == 'Capped-25':
            weights = assets['market_cap'] / assets['market_cap'].sum()
            weights = np.where(weights > 0.25, 0.25, weights)
            excess_weight = 1 - weights.sum()
            weights += (weights / weights.sum()) * excess_weight  # Redistribute proportionally
        elif scheme == 'Proportional':
            weights = assets['market_cap'] / assets['market_cap'].sum()
        elif scheme == 'Square Root':
            weights = np.sqrt(assets['market_cap'])
            weights /= weights.sum()
        else:
            raise ValueError("Unknown weighting scheme.")
        return weights

    def calculate_portfolio_value(current_composition, day_data):
        return sum(comp['units'] * day_data[day_data['coin_id'] == comp['coin_id']]['price'].values[0] for comp in current_composition if comp['coin_id'] in day_data['coin_id'].values)

    output = []
    for single_date in pd.date_range(start=start_date, end=end_date):
        if single_date in rebalance_dates or single_date == start_date:
            day_before = single_date - timedelta(days=1) if single_date != start_date else single_date
            assets = df[(df['timestamp'] == day_before) & (df['market_cap'] >= minimum_market_cap)].nlargest(max_number_of_components, 'market_cap')
            weights = apply_weighting_scheme(assets, weighting_scheme)
            current_composition = [{'coin_id': row.coin_id, 'units': (portfolio_value * weight / row.price)} for row, weight in zip(assets.itertuples(), weights)]
        
        day_data = df[df['timestamp'] == single_date]
        if not day_data.empty:
            portfolio_value = calculate_portfolio_value(current_composition, day_data)

        output.append({'date': single_date, 'portfolio_value': portfolio_value})

    return pd.DataFrame(output)

