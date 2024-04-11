import requests
import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import linregress


def get_alpha_vantage_data(symbol, api_key):
    # Replace FUNCTION with the desired Alpha Vantage function, e.g., TIME_SERIES_DAILY
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Process your data here
        print(data)
    else:
        print("Failed to retrieve data from Alpha Vantage")

def get_yahoo_finance_data(symbol):
    stock = yf.Ticker(symbol)
    # Get historical market data
    hist = stock.history(period="1mo")  # 1 month of data
    print(hist)



def get_stock_beta(stock_symbol, market_symbol, start_date, end_date):
    # Fetch historical data
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    market_data = yf.download(market_symbol, start=start_date, end=end_date)
    
    # Calculate daily returns
    stock_returns = stock_data['Adj Close'].pct_change()[1:]
    market_returns = market_data['Adj Close'].pct_change()[1:]
    
    # Align dates for stock and market data
    aligned_data = pd.concat([stock_returns, market_returns], axis=1).dropna()
    aligned_data.columns = ['Stock Returns', 'Market Returns']
    
    # Perform linear regression to calculate beta
    beta, intercept, r_value, p_value, std_err = linregress(aligned_data['Market Returns'], aligned_data['Stock Returns'])
    
    return beta

if __name__ == "__main__":
    stock_symbol = 'AAPL'
    market_symbol = '^GSPC'  # S&P 500
    start_date = '2020-01-01'
    end_date = '2021-01-01'
    
    beta = get_stock_beta(stock_symbol, market_symbol, start_date, end_date)
    print(f"The beta of {stock_symbol} relative to {market_symbol} from {start_date} to {end_date} is: {beta:.2f}")

    ALPHA_VANTAGE_API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'
    symbol = 'AAPL'  # Example stock symbol

    #get_alpha_vantage_data(symbol, ALPHA_VANTAGE_API_KEY)
    #get_yahoo_finance_data(symbol)
