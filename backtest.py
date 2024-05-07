import pandas as pd
import numpy as np
from datetime import timedelta

# Backtesting loop
def perform_backtest(df, start_date, end_date, weighting_scheme, max_number_of_components, rebalance_frequency, initial_portfolio_value=100):
    if 'timestamp' not in df.columns:
        raise ValueError("Timestamp column missing from the DataFrame")
    # Sort the DataFrame for consistency
    df.sort_values(by=['timestamp', 'coin_id'], inplace=True)

    # Initialize portfolio value and composition
    portfolio_value = initial_portfolio_value
    current_composition = []

    # Frequency to pandas frequency
    freq_map = {'Daily': 'D', 'Monthly': 'MS', 'Quarterly': 'QS-JAN'}
    rebalance_dates = pd.date_range(start=start_date, end=end_date, freq=freq_map[rebalance_frequency])

    # Function to apply weighting scheme
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

    # Function to adjust weights for Capped-25 repeatedly until no component exceeds 25%
    def adjust_weights_for_capped(weights):
        while any(weights > 0.25):
            excess_weights = np.where(weights > 0.25, weights - 0.25, 0)
            total_excess = excess_weights.sum()
            weights = np.where(weights <= 0.25, weights + (excess_weights / weights.sum()) * total_excess, 0.25)
        return weights

    # Calculate portfolio value
    def calculate_portfolio_value(current_composition, day_data):
        portfolio_value = sum(comp['units'] * day_data[day_data['coin_id'] == comp['coin_id']]['price'].values[0] for comp in current_composition if comp['coin_id'] in day_data['coin_id'].values)
        return portfolio_value

    # Backtesting loop
    output = []
    for single_date in pd.date_range(start=start_date, end=end_date):
        if single_date in rebalance_dates or single_date == start_date:
            day_before = single_date - timedelta(days=1) if single_date != start_date else single_date
            assets = df[(df['timestamp'] == day_before)].nlargest(max_number_of_components, 'market_cap')
            weights = apply_weighting_scheme(assets, weighting_scheme)
            if weighting_scheme == 'Capped-25':
                weights = adjust_weights_for_capped(weights)
            current_composition = [{'coin_id': row.coin_id, 'units': (portfolio_value * weight / row.price)} for row, weight in zip(assets.itertuples(), weights)]

        day_data = df[df['timestamp'] == single_date]
        if not day_data.empty:
            portfolio_value = calculate_portfolio_value(current_composition, day_data)

        output.append({'date': single_date, 'composition': [(comp['coin_id'], comp['units']) for comp in current_composition], 'portfolio_value': portfolio_value})

    output_df = pd.DataFrame(output)
    return output_df
