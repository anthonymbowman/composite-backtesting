import pandas as pd
import itertools
from backtest_mod import run_backtest

# Load your DataFrame here
df = pd.read_csv('crypto_data.csv')  # Adjust the path as necessary

# Parameters for the simulation
weighting_schemes = ['Equal', 'Capped-25', 'Proportional', 'Square Root']
max_components_options = [5, 10, 20, 50]
rebalance_frequencies = ['Monthly', 'Quarterly']

# Initialize an empty DataFrame for results
results = pd.DataFrame()

# Run simulations for all combinations of parameters
for weighting_scheme, max_components, rebalance_frequency in itertools.product(weighting_schemes, max_components_options, rebalance_frequencies):
    # Corrected call to run_backtest with DataFrame as the first argument
    simulation_result = run_backtest(df, weighting_scheme, max_components, 1e8, rebalance_frequency)

    # Assuming simulation_result returns a DataFrame with 'date' and 'portfolio_value'
    simulation_result.set_index('date', inplace=True)

    # Rename the 'portfolio_value' column to reflect the simulation parameters
    column_name = f"{weighting_scheme}_{max_components}_{rebalance_frequency}"
    simulation_result.rename(columns={'portfolio_value': column_name}, inplace=True)

    # Merge this simulation's result into the results DataFrame
    if results.empty:
        results = simulation_result
    else:
        results = results.join(simulation_result, how='outer')

# Reset the index to add 'date' back as a column and prepare for CSV export
results.reset_index(inplace=True)
results.rename(columns={'index': 'Date'}, inplace=True)

# Export the combined results to a CSV file
results.to_csv('backtest_simulations_combined_results.csv', index=False)
