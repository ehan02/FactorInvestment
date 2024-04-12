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

