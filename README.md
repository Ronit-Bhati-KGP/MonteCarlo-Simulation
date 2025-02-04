Monte Carlo Stock Portfolio Simulation
Overview
This project implements a Monte Carlo simulation to model the future value of a stock portfolio. The simulation considers multiple assets, their historical returns, and covariance to generate possible future portfolio values.

Features

- Retrieves stock data using the yfinance library.

- Calculates daily returns, mean returns, and covariance matrix of selected stocks.

- Implements Monte Carlo simulations to predict portfolio value over time.

- Uses Cholesky decomposition for realistic correlated asset return modeling.

- Plots simulation results to visualize portfolio performance.

- Computes Value at Risk (VaR) and Conditional Value at Risk (CVaR) to assess portfolio risk.

- Saves the output plot of the simulation for further analysis.

Libraries Used

The project uses the following Python libraries:

numpy - For numerical calculations, including random sampling and matrix operations.

pandas - For handling stock data, calculating returns, and managing data structures.

yfinance - To fetch historical stock data from Yahoo Finance.

matplotlib - For visualizing the Monte Carlo simulation results.

time - To introduce a slight delay in data retrieval to avoid API rate limits.

