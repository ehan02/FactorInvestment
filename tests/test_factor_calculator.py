import pytest
import pandas as pd
from library.factor_calculator import PEFactorCalculator, PBFactorCalculator, EVToEBITDAFactorCalculator

# Example data for testing
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'MarketPrice': [100, 200, 150],
        'EarningsPerShare': [10, 20, 15],
        'BookValuePerShare': [50, 100, 75],
        'EnterpriseValue': [1000, 2000, 1500],
        'EBITDA': [100, 200, 150]
    })

def test_pe_factor_calculator(sample_data):
    calculator = PEFactorCalculator(sample_data)
    expected_pe = sample_data['MarketPrice'] / sample_data['EarningsPerShare']
    pd.testing.assert_series_equal(calculator.calculate_factors(), expected_pe)

def test_pb_factor_calculator(sample_data):
    calculator = PBFactorCalculator(sample_data)
    expected_pb = sample_data['MarketPrice'] / sample_data['BookValuePerShare']
    pd.testing.assert_series_equal(calculator.calculate_factors(), expected_pb)

def test_ev_to_ebitda_factor_calculator(sample_data):
    calculator = EVToEBITDAFactorCalculator(sample_data)
    expected_ev_to_ebitda = sample_data['EnterpriseValue'] / sample_data['EBITDA']
    pd.testing.assert_series_equal(calculator.calculate_factors(), expected_ev_to_ebitda)
 
