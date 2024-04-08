# Index Coop Composite Strategy Backtesting Application

## Overview

This project is dedicated to developing a user-friendly tool for backtesting investment strategies within specific sectors or themes, based on predefined methodologies. It aims to facilitate the visualization of historical performance, aiding in the product development process and providing valuable insights for Index Coop Informational Indices (ICII).

## Features

- **Asset Selection**: Users can choose from a list of whitelisted assets sourced from CoinGecko, representing a curated universe of eligible investments.
- **Customizable Backtesting Parameters**: Options for setting the backtest start date, methodology, rebalance schedule, benchmark asset, and other relevant parameters.
- **Comprehensive Data Utilization**: Utilizes daily price data, circulating market capitalization (CMC), total supply, and fully diluted valuation (FDV) for in-depth analysis.
- **Result Comparison**: Facilitates direct comparison between the backtested strategy's performance and a chosen benchmark.

### Detailed Inputs:

- **Eligible Assets**: Selection from a predefined, whitelisted universe.
- **Start Date**: Customizable initiation point for backtesting.
- **Rebalance Cadence**: Options for monthly, quarterly, or annually adjustments.
- **Methodology**: Selection from a list of pre-defined strategies.
- **Max Assets**: Limit on the number of assets within the strategy.
- **Minimum Market Capitalisation**: Threshold for asset eligibility based on market cap.
- 

## Application Structure

- **Title**: Index Coop Composite Backtester
- **Eligible Asset Universe Selection**:
    - Search and filter functionality to locate specific assets.
    - Dual-column layout for asset selection: "Unselected Assets" and "Selected Assets", facilitating easy organization.
- **Methodology Configuration**:
    - Dropdown menu for methodology selection, accompanied by concise descriptions of each methodology.
- **Restrictions**:
    - Slider and input fields for setting the maximum number of assets and minimum market cap requirement.
- **Rebalancing Setup**:
    - Date and time inputs to define the start and cadence of the rebalancing process.
- **Results**:
    - Historical Net Asset Value vs. Benchmark
    - Finanical metrics such as volatility, Sharpe Ratio, Sorintino Ratio, Beta, Correlation    

## Methodologies

- **Equal Weighting**: Distributes investment evenly across all selected assets.
- **Circulating Market Capitalisation**: Weights investments proportionally to the circulating market capitalization of each asset.
- **Capped 25% Circulating MC**: Similar to Circulating Market Cap, but caps any single asset's weight at 25%, redistributing excess proportionally.
- **Square Root Market Cap**: Assigns weight based on the square root of each asset's circulating market cap, balancing influence between large and small cap assets.

## Data Sources

Utilizes CoinGecko's API for up-to-date financial data, including:
- Coin Historic Chart Data by ID
- Coins List (ID Map)
- Search

## Enhancements

- **Simulation**: Include a feature for simulating future performance based on historical volatility and trends.
- **User Profiles**: Allow users to save and revisit their backtesting configurations and results.
- **Advanced Filtering**: Enhance the asset selection process with more sophisticated filters (e.g., sector, performance criteria).
- **Interactive Results**: Dynamic charts and graphs to visualize backtesting outcomes and comparisons with benchmarks.
- **API Integration Best Practices**: Ensure efficient and respectful use of the CoinGecko API to maintain service integrity and responsiveness.




