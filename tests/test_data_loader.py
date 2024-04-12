# tests/test_data_handler.py
import pandas as pd
from pathlib import Path
from factor_investment.data_loader import DataLoader

# Get the directory where the script is located (not necessarily where it's run from)
base_path = Path(__file__).parent
data_file = base_path /  'exposure_trade.csv'

def test_data_loader():
    loader = DataLoader(data_file)
    data = loader.load_data()
    assert not data.empty

