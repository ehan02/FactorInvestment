import pandas as pd

# Load data
df = pd.read_csv("stock_data.csv")

# Calculate Momentum Factor: We'll use 12-month price returns as a proxy for momentum.
df['Momentum'] = (df['Price_t'] / df['Price_t-12']) - 1

# Calculate Growth Factor: Directly using the 'EarningsGrowth' column
df['Growth'] = df['EarningsGrowth']

# Normalize the factors to have a common scale
df['Momentum_Score'] = (df['Momentum'] - df['Momentum'].mean()) / df['Momentum'].std()
df['Growth_Score'] = (df['Growth'] - df['Growth'].mean()) / df['Growth'].std()

# Combine the factors with equal weights
df['Combined_Score'] = 0.5 * df['Momentum_Score'] + 0.5 * df['Growth_Score']

# Select Top N Stocks based on Combined Score
N = 10  # Number of stocks to select
top_stocks = df.nlargest(N, 'Combined_Score')

print(top_stocks[['Ticker', 'Combined_Score']])
