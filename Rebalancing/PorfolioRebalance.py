import pandas as pd

# Example portfolio holdings and current prices
# For simplicity, assume we only have two assets: stocks and bonds
portfolio = {
    'Asset': ['Stocks', 'Bonds'],
    'Quantity': [100, 200],  # Quantity of each asset
    'CurrentPrice': [150, 110],  # Current price of each asset
    'TargetAllocation': [0.6, 0.4],  # Target allocation for each asset
}

# Convert to DataFrame
portfolio_df = pd.DataFrame(portfolio)

# Calculate current value and total portfolio value
portfolio_df['CurrentValue'] = portfolio_df['Quantity'] * portfolio_df['CurrentPrice']
total_portfolio_value = portfolio_df['CurrentValue'].sum()

# Calculate current allocation percentage for each asset
portfolio_df['CurrentAllocation'] = portfolio_df['CurrentValue'] / total_portfolio_value

# Determine the amount to buy/sell to reach target allocation
portfolio_df['TargetValue'] = total_portfolio_value * portfolio_df['TargetAllocation']
portfolio_df['Adjustment'] = portfolio_df['TargetValue'] - portfolio_df['CurrentValue']

# Calculate the quantity to buy/sell for each asset
portfolio_df['AdjustmentQuantity'] = portfolio_df['Adjustment'] / portfolio_df['CurrentPrice']

# Display the adjustments needed
print("Portfolio Rebalancing Adjustments:")
print(portfolio_df[['Asset', 'AdjustmentQuantity']])

# Optionally, round AdjustmentQuantity if dealing with whole units like stocks
portfolio_df['AdjustmentQuantity'] = portfolio_df['AdjustmentQuantity'].round()

print("\nRounded Adjustments (for whole units):")
print(portfolio_df[['Asset', 'AdjustmentQuantity']])
