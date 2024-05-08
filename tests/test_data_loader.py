import sys
sys.path.append(f"C:/Users/hmhan/Documents/Code/FactorInvestment")

import asyncio
import pandas as pd
from pathlib import Path
from factor_investment.data_loader import DataLoader

# Get the directory where the script is located (not necessarily where it's run from)
base_path = Path(__file__).parent
data_file = base_path /  'exposure_trade.csv'

API_KEY = '4GLXNSBY9QNYX77M'
companies = ['AAPL']
base_url = "https://www.alphavantage.co/query?"

class TestDataLoader:
    def __init__(self, loader):
        self.loader = loader

    # def test_data_loader_csv():
    #     loader = DataLoader('csv', data_file)
    #     data = loader.load_data()
    #     assert not data.empty


    async def get_stock_data(self, ticker):
        """Fetches historical stock data for a given ticker using DataLoader."""
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
        df = df.astype(float)
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
        """Run tests to fetch data for all companies."""
        for company in companies:
            stock_data = await self.get_stock_data(company)
            financial_data = await self.get_financial_data(company)
            print(f"Stock Data for {company}:")
            print(stock_data.head())  # Display first few rows of the stock data
            print(f"Financial Data for {company}:")
            print(financial_data)  # Print the financial data

            # Save data to CSV (optional)
            stock_data.to_csv(f"{company}_stock_data.csv")
            pd.DataFrame(financial_data['annualReports']).to_csv(f"{company}_financial_data.csv")

# Setup DataLoader and TestDataLoader
data_loader = DataLoader(config_file='config.json')  # Assuming you have a suitable config.json
test_loader = TestDataLoader(data_loader)

# Run the test class
asyncio.run(test_loader.run_tests())
