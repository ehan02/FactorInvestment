import json
import pandas as pd
import logging
import aiohttp
import aiofiles
import asyncio
from pathlib import Path,WindowsPath, PosixPath
from typing import Any, Dict
from factor_investment.log_config import setup_logging

class DataLoader:
    def __init__(self, config_file=None):
        setup_logging(config_file)  # Set up logging configuration
        if config_file:
            self.load_config(config_file)
        self.cache = {}

    def load_config(self, config_file):
        """
        Load configuration from a JSON file.
        """
        with open(config_file, 'r') as file:
            config = json.load(file)
        self.api_key = config.get('api_key', '') 
        self.base_url = config.get('base_url', '')  # Base URL for the API

    async def load_data(self, data_source_type, source_path):
        """
        Asynchronously load data from the configured source.
        """
        cache_key = str(source_path)
        if cache_key in self.cache:
            logging.info("Data loaded from cache.")
            return self.cache[cache_key]

        if Path(source_path).suffix == '.csv':
            data = await self._load_from_csv(source_path)
        elif source_path.startswith(('http', 'https')):
            data = await self._load_from_api(source_path)
        else:
            raise ValueError("Invalid source. Provide a valid CSV file path or API URL.")

        self.cache[cache_key] = data
        return data

    async def _load_from_csv(self, source_path):
        """
        Asynchronously load data from a CSV file.
        """
        try:
            async with aiofiles.open(source_path, mode='r') as file:
                data = await file.read()
            df = pd.read_csv(pd.compat.StringIO(data))
            logging.info(f"Data loaded successfully from {source_path}")
            return df
        except Exception as e:
            logging.error(f"An error occurred while reading CSV: {e}")
            raise

    async def _load_from_api(self, source_path):
        """
        Asynchronously load data from an API.
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(source_path) as response:
                    response.raise_for_status()
                    data = await response.json()
                #df = pd.DataFrame(data)
                logging.info(f"Data loaded successfully from {source_path}")
                return data
            except Exception as e:
                logging.error(f"An error occurred while fetching API data: {e}")
                raise

# Example usage:
# loader = DataLoader(config_file='config.json')
# data = asyncio.run(loader.load_data('api', 'http://example.com/api/data'))
# print(data)
