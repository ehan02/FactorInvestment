import pandas as pd
import numpy as np

# Simulated historical stock prices data
data = {
    'AAPL': [150, 152, 155, 157, 160, 162, 164, 165, 170, 172,175],
    'GOOGL': [2725, 2710, 2730, 2750, 2770, 2790, 2780, 2760, 2750, 2775,2776],
    'AMZN': [3100, 3120, 3140, 3130, 3150, 3170, 3190, 3200, 3210, 3230,3567]
}

# Convert dictionary to DataFrame
prices = pd.DataFrame(data)

# Moving averages
short_window = 3
long_window = 5

# Calculate short-term and long-term moving averages
short_rolling = prices.rolling(window=short_window).mean()
long_rolling = prices.rolling(window=long_window).mean()

# Generate signals based on the moving averages
# Buy signal (1): short-term average crosses above long-term average
# Sell signal (-1): short-term average crosses below long-term average
signals = np.where(short_rolling > long_rolling, 1, -1)

# Handling NaN values with forward fill method to avoid initial NaN values from rolling mean
signals_df = pd.DataFrame(signals, columns=prices.columns, index=prices.index).fillna(method='ffill')

print("Price Data:") 
print(prices)
print("\nShort-Term Moving Average:")
print(short_rolling)
print("\nLong-Term Moving Average:")
print(long_rolling)
print("\nTrading Signals (-1 = sell, 1 = buy):")
print(signals_df)
