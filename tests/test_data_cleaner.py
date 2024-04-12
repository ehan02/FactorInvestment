# tests/test_data_handler.py
import pandas as pd
from factor_investment.data_cleaner import DataCleaner
import pytest

def test_data_cleaner():
    df = pd.DataFrame({'col1': [1, 2, None, 4], 'col2': [4, None, 6, 8]})
    cleaner = DataCleaner(df)
    cleaned_data = cleaner.clean_data()
    assert not cleaned_data.isnull().values.any()
