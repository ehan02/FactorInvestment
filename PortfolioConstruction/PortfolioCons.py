import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Sample historical price data for a few stocks
data = {
    'AAPL': [150, 152, 154, 153, 155],
    'MSFT': [210, 211, 209, 208, 207],
    'GOOGL': [2720, 2730, 2740, 2735, 2745],
    'AMZN': [3300, 3320, 3310, 3325, 3330]
}

# Convert the dictionary to a DataFrame
prices = pd.DataFrame(data)

# Calculate daily returns
returns = prices.pct_change().dropna()

# Mean returns and covariance
mean_returns = returns.mean()
cov_matrix = returns.cov()

# Number of assets
num_assets = len(mean_returns)

# Portfolio performance function
def portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.dot(weights, mean_returns)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return returns, volatility

# Objective function (minimize volatility)
def minimize_volatility(weights, mean_returns, cov_matrix):
    return portfolio_performance(weights, mean_returns, cov_matrix)[1]

# Constraints (weights sum to 1)
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

# Bounds for weights
bounds = tuple((0, 1) for asset in range(num_assets))

# Initial guess (equal distribution)
init_guess = num_assets * [1. / num_assets,]

# Minimize volatility
optimal_weights = minimize(minimize_volatility, init_guess, args=(mean_returns, cov_matrix), method='SLSQP', bounds=bounds, constraints=constraints)

# Optimal portfolio
opt_returns, opt_volatility = portfolio_performance(optimal_weights.x, mean_returns, cov_matrix)
print(f"Optimal Portfolio Returns: {opt_returns}")
print(f"Optimal Portfolio Volatility: {opt_volatility}")

# Plotting
plt.figure(figsize=(10, 5))
plt.scatter(opt_volatility, opt_returns, marker='*', color='r', s=200, label='Optimal Portfolio')
plt.title('Portfolio Optimization')
plt.xlabel('Volatility')
plt.ylabel('Returns')
plt.legend(labelspacing=0.8)
plt.show()
