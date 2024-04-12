import pytest
import pandas as pd
from factor_investment.factor_calculator import FactorCalculator

@pytest.fixture
def sample_data():
    data = pd.DataFrame({
        'price': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109]
    })
    return data

def test_calculate_momentum(sample_data):
    calculator = FactorCalculator(sample_data)
    result = calculator.calculate_momentum()
    assert 'momentum' in result.columns
    #assert result['momentum'].iloc[-1] == pytest.approx(0.02912621, 0.01)

def test_calculate_volatility(sample_data):
    calculator = FactorCalculator(sample_data)
    result = calculator.calculate_volatility()
    assert 'volatility' in result.columns
    assert result['volatility'].iloc[-1] is not None
