import pandas as pd
import numpy as np
import requests
import logging
from pathlib import WindowsPath,PosixPath
from typing import Any, Dict

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DataLoader:
    _instance = None

    def __new__(cls, data_source_type: str, source_path: str):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
            cls._instance.data_source_type = data_source_type
            cls._instance.source_path = source_path
        return cls._instance

    def load_data(self) -> Any:
        """ Load data based on the data source type (CSV or API). """
        if self.data_source_type == 'csv':
            return self.load_from_csv(self.source_path)
        elif self.data_source_type == 'api':
            return self.load_from_api(self.source_path)
        else:
            logging.error("Unsupported data source type provided.")
            raise ValueError("Unsupported data source type. Use 'csv' or 'api'.")

    def load_data(self):
        """
        Load data from the specified source, which could be a file path or an API URL.
        """
        if isinstance(self.source_path, WindowsPath) or isinstance(self.source_path, PosixPath) :
            return self._load_from_csv()
        elif self.source_path.endswith('.csv'):
            return self._load_from_csv()
        elif self.source_path.startswith(('http', 'https')):
            return self._load_from_api()
        else:
            raise ValueError("Invalid source. Provide a valid CSV file path or API URL.")

    def _load_from_csv(self):
        """
        Private method to load data from a CSV file.
        """
        try:
            data = pd.read_csv(self.source_path)
            print(f"Data loaded successfully from {self.source_path}")
            return data
        except FileNotFoundError:
            print(f"Error: The file at {self.source_path} was not found.")
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
            response = requests.get(self.source_path)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = pd.DataFrame(response.json())  # Adjust this depending on the structure of the API response
            print(f"Data loaded successfully from {self.source_path}")
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

