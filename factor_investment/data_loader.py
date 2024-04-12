import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
import requests
from pathlib import WindowsPath

class DataLoader:

    def __init__(self, source):
        self.source = source

    def load_data(self):
        """
        Load data from the specified source, which could be a file path or an API URL.
        """
        if isinstance(self.source, WindowsPath):
            return self._load_from_csv()
        elif self.source.endswith('.csv'):
            return self._load_from_csv()
        elif self.source.startswith(('http', 'https')):
            return self._load_from_api()
        else:
            raise ValueError("Invalid source. Provide a valid CSV file path or API URL.")

    def _load_from_csv(self):
        """
        Private method to load data from a CSV file.
        """
        try:
            data = pd.read_csv(self.source)
            print(f"Data loaded successfully from {self.source}")
            return data
        except FileNotFoundError:
            print(f"Error: The file at {self.source} was not found.")
            raise
        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def _load_from_api(self):
        """
        Private method to load data from a financial API.
        """
        try:
            response = requests.get(self.source)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = pd.DataFrame(response.json())  # Adjust this depending on the structure of the API response
            print(f"Data loaded successfully from {self.source}")
            return data
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving data from API: {e}")
            raise
        except ValueError as e:
            print(f"Error processing data: {e}")
            raise


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
