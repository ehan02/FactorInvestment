import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
import requests

class DataCleaner:

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def clean_data(self):
       
        if self.dataframe.empty:
            print("Warning: The dataframe is empty.")
            return self.dataframe

        cleaned_data = self.dataframe.dropna()
        print(f"Removed {len(self.dataframe) - len(cleaned_data)} rows with missing values.")

        return cleaned_data