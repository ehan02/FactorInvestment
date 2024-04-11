import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm

def fetch_data(symbols, start_date, end_date):
    """Fetch historical stock data and market index data."""
    data = yf.download(symbols, start=start_date, end=end_date)
    return data['Adj Close']

def calculate_beta(stock_returns, market_returns):
    """Calculate beta of stocks based on market returns."""
    stock_returns = stock_returns.dropna()
    market_returns = market_returns.dropna()
    X = sm.add_constant(market_returns)  # Adds a constant term to the predictor
    model = sm.OLS(stock_returns, X).fit()
    return model.params[1]

def calculate_factors(stock_data, market_symbol):
    """Calculate beta, value (P/E ratio), and momentum factors."""
    market_returns = stock_data[market_symbol].pct_change()
    factors = pd.DataFrame(index=stock_data.columns)
    
    for symbol in stock_data.columns:
        if symbol == market_symbol:
            continue
        stock_returns = stock_data[symbol].pct_change()
        factors.loc[symbol, 'Beta'] = calculate_beta(stock_returns, market_returns)
        stock_info = yf.Ticker(symbol).info
        factors.loc[symbol, 'PE_Ratio'] = stock_info.get('forwardPE', np.nan)
        factors.loc[symbol, 'Momentum'] = stock_data[symbol].pct_change(periods=120).iloc[-1]  # 6-month momentum
    
    factors['Value'] = 1 / factors['PE_Ratio']  # Inverse of P/E ratio for value
    return factors.dropna()

def select_stocks(factors, top_n=10):
    """Select top N stocks based on factors."""
    # Normalize factors
    print(top_n)
    factors['Beta_Score'] = 1 - (factors['Beta'] - factors['Beta'].min()) / (factors['Beta'].max() - factors['Beta'].min())
    factors['Value_Score'] = (factors['Value'] - factors['Value'].min()) / (factors['Value'].max() - factors['Value'].min())
    factors['Momentum_Score'] = (factors['Momentum'] - factors['Momentum'].min()) / (factors['Momentum'].max() - factors['Momentum'].min())
    
    # Composite score
    factors['Composite_Score'] = factors[['Beta_Score', 'Value_Score', 'Momentum_Score']].mean(axis=1)
    
    # Select top N stocks
    selected_stocks = factors.nlargest(top_n, 'Composite_Score')
    return selected_stocks.index.tolist()

if __name__ == '__main__':
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA','NVO','LLY','TSM','AVGO','JPM', '^GSPC']  # Example symbols + S&P 500 as market
    start_date = '2020-01-01'
    end_date = '2021-01-01'
    
    stock_data = fetch_data(symbols, start_date, end_date)
    factors = calculate_factors(stock_data, '^GSPC')
    selected_stocks = select_stocks(factors,3)
    
    print("Selected Stocks:", selected_stocks)
