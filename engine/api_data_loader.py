import sys
sys.path.append(f"C:/Users/hmhan/Documents/Code/FactorInvestment")
import csv
import asyncio
import pandas as pd
from pathlib import Path
from library.data_loader import DataLoader

# Get the directory where the script is located (not necessarily where it's run from)
base_path = Path(__file__).parent
data_file = base_path /  'exposure_trade.csv'

API_KEY = '4GLXNSBY9QNYX77M'
companies = ['AAPL']
base_url = "https://www.alphavantage.co/query?"

class APIDataLoader:
    def __init__(self, loader):
        self.loader = loader

    async def get_stock_data(self, ticker):
        """Fetchesdata historical stock data for a given ticker using DataLoader."""
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': ticker,
            'outputsize': 'full',
            'apikey': API_KEY
        }
        url = f"{base_url}&" + "&".join(f"{key}={value}" for key, value in params.items())
        data = await self.loader.load_data(data_source_type='api', source_path=url)
        df = pd.DataFrame(data['Time Series (Daily)']).T
        df.rename(columns=lambda x: x[3:], inplace=True)
        #df = df.astype(float)
        return df

    async def get_financial_data(self, ticker):
        """Fetches financial data for a given ticker using DataLoader."""
        params = {
            'function': 'INCOME_STATEMENT',
            'symbol': ticker,
            'apikey': API_KEY
        }
        url = f"{base_url}&" + "&".join(f"{key}={value}" for key, value in params.items())
        data = await self.loader.load_data(data_source_type='api', source_path=url)
        return data

    async def run_tests(self):
        """Run tests to fetch data for all companies and write to the same file."""
        all_stock_data = []
        all_financial_data = []

        for company in companies:
            stock_data = await self.get_stock_data(company)
            financial_data = await self.get_financial_data(company)

            print(f"Stock Data for {company}:")
            print(stock_data.head())  # Display first few rows of the stock data
            print(f"Financial Data for {company}:")
            print(financial_data)  # Print the financial data

            stock_data['Company'] = company
            all_stock_data.append(stock_data)

            financial_data['Company'] = company
            all_financial_data.append(financial_data)
 
        all_stock_data = pd.DataFrame(all_stock_data[0])        
        #all_financial_data = pd.DataFrame(all_financial_data)
        # # Concatenate all data into a single DataFrame
        #combined_stock_data = pd.concat(all_stock_data)
        # combined_financial_data = pd.concat(all_financial_data)
        print(all_financial_data.shape())

        # Save the combined data to CSV files
        all_stock_data.to_csv("stock_data.csv")
        all_financial_data.to_csv("financial_data.csv")
                

# Setup DataLoader and APIDataLoader
data_loader = DataLoader(config_file='config.json')  
api_data_loader = APIDataLoader(data_loader)

# Run the test class
asyncio.run(api_data_loader.run_tests())
