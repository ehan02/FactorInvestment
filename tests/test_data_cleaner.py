import pandas as pd
import numpy as np
from factor_investment.data_cleaner import FillMissingDataStrategy, WinsorizationStrategy, DataCleaner

def test_fill_missing_data():
    # Create sample data with missing values
    data = pd.DataFrame({
        'asset_returns': [10, np.nan, 30, 40, 50],
        'volumes': [np.nan, 200, np.nan, 400, 500]
    })
    expected_filled = pd.DataFrame({
        'asset_returns': [10, 35, 30, 40, 50],
        'volumes': [400, 200, 400, 400, 500]
    })

    strategy = FillMissingDataStrategy()
    result = strategy.apply(data.copy()).astype(np.int64)
    print(result)

    pd.testing.assert_frame_equal(result, expected_filled)

def test_winsorization():
    # Create sample data with outliers
    data = pd.DataFrame({
        'asset_returns': [1, 2, 3, 10, 5, 6, 7, 8, 9, 10],
        'volumes': [100, 200, 300, 400, 500, 600, 700, 800, 900, 10000]
    })
    expected_winsorized = pd.DataFrame({
        'asset_returns': [1, 2, 3, 10, 5, 6, 7, 8, 9, 10],
        'volumes': [145, 200, 300, 400, 500, 600, 700, 800, 900, 5904]
    })

    strategy = WinsorizationStrategy(0.05, 0.95)
    result = strategy.apply(data.copy()).astype(np.int64)
    print(result)
    pd.testing.assert_frame_equal(result, expected_winsorized)

def test_data_cleaner():
    # Integrate both strategies
    data = pd.DataFrame({
        'asset_returns': [10, np.nan, 30, 300, 50],
        'volumes': [np.nan, 200, np.nan, 400, 10000]
    })
    expected_cleaned = pd.DataFrame({
        'asset_returns': [14, 40, 30, 249, 50],
        'volumes': [400, 240, 400, 400, 8079]
    })

    strategies = [FillMissingDataStrategy(), WinsorizationStrategy(0.05, 0.95)]
    cleaner = DataCleaner(strategies)
    result = cleaner.clean_data(data.copy()).astype(np.int64)
    print(result)
    pd.testing.assert_frame_equal(result, expected_cleaned)

