import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CleaningStrategy:
    """Interface for data cleaning strategies."""
    def apply(self, data):
        raise NotImplementedError("Cleaning strategy must implement the apply method.")

class FillMissingDataStrategy(CleaningStrategy):
    """Strategy to fill missing data with the median of each column."""
    def apply(self, data):
        for column in data.columns:
            if data[column].isnull().any():
                median_value = data[column].median()
                data[column].fillna(median_value, inplace=True)
                logging.info(f"Missing values in {column} filled with median value {median_value}.")
        return data

class WinsorizationStrategy(CleaningStrategy):
    """Strategy to apply Winsorization to limit extreme values using percentiles."""
    def __init__(self, lower_percentile=0.01, upper_percentile=0.99):
        self.lower_percentile = lower_percentile
        self.upper_percentile = upper_percentile

    def apply(self, data):
        quantiles = data.quantile([self.lower_percentile, self.upper_percentile])
        for column in data.columns:
            if pd.api.types.is_numeric_dtype(data[column]):
                original_data = data[column].copy()  # For logging purposes
                data[column] = np.where(data[column] < quantiles.loc[self.lower_percentile, column], 
                                        quantiles.loc[self.lower_percentile, column], data[column])
                data[column] = np.where(data[column] > quantiles.loc[self.upper_percentile, column], 
                                        quantiles.loc[self.upper_percentile, column], data[column])
                changed_values = original_data[original_data != data[column]]
                logging.info(f"Winsorized {len(changed_values)} values in column {column}.")
        return data

class DataCleaner:
    """Applies multiple data cleaning strategies to a DataFrame."""
    def __init__(self, strategies):
        self.strategies = strategies

    def clean_data(self, data):
        for strategy in self.strategies:
            data = strategy.apply(data)
        return data
