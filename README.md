# Index Coop Composite Strategy Backtesting App

## Overview

This project aims to create a simple tool for backtesting strategies to see the historical performance of a sector or theme according to a preset methodology. It will be used during the product development process to illustrate historical returns. It will also be used by Index Coop Informational Indices (ICII).

## Features

The user should be able to select a variety of whitelisted assets from CoinGecko’s token list representing the eligible asset universe. Then, the user will select a backtest start date, a methodology from a list of pre-designed methodologies, and a rebalance schedule. The user will also be able to select a benchmark asset. The application will fetch the daily price, circulating market capitalisation (CMC), and total supply and, from the price and total supply, derive a fully diluted valuation (FDV).

The application will then run a backtest from the start date utilizing the eligible asset universe, the selected methodology, and rebalance cadence.

The application will return the results of the backtest versus the benchmark.

Inputs:
- Eligible Assets
- Start Date
- Rebalance Cadence
- Methodology
- Circulating Market Capitalization
- Fully Diluted Valuation


- Max Assets
- Minimum Market Capitalisation

## App Structure:

Title: Index Coop Composite Backtester
Header: Eligible Asset Universe

Search Bar: Search for Assets
Two columns: Unselected Assets, Selected Assets
/*
The user should be presented with a list of all assets in "Unselected Assets"
Then they should be able to add an asset to "Selected Assets"
They should be able to move an asset from "Unselected Assets" to "Selected Assets"
*/

Button: Save Assets --> Fetch price, cmc, total supply for each asset daily. calculate FDV daily.

Header: Choose Methodology
Single Select Dropdown: {list of eligible methodologies}
Header: Restrictions
Number Input (Slider): Max Assets
Number Input: Min Market Cap

Header: Rebalancing
Date Input: Start Date
Single Select Dropdown: Cadence (Monthly, Quarterly, Annually)
Time Input: Rebalance Time

## Methodologies

- Equal: Weight each component equally as long as it is eligible.
- Circulating Market Capitalisation: Weight each component according to its Circ. MC
- Capped 25% Circulating MC: Same as Circ. Market Cap, but if a component has a weight > 30%, lower it to 25% and distribute the remaining amount proportionally to eligible strategies
- Square Root Market Cap: Weight each component accord to the square root of its circulating market cap
  
## Data Sources

CoinGecko API:
- [Coin Historic Chart Data by ID](https://docs.coingecko.com/reference/coins-id-market-chart)
- [Coins List (ID Map)](https://docs.coingecko.com/reference/coins-list)
- [Search](https://docs.coingecko.com/reference/search-data)




