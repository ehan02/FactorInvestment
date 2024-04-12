import pytest
import pandas as pd
from run_analysis import run_analysis

@pytest.fixture
def mock_data():
    return pd.DataFrame({
        'price': [100, 101, 102, 105, 108, 110, 115, 120, 125, 130]
    })

def test_run_analysis(mocker, mock_data):
    # Setup mocks
    mock_loader = mocker.patch('run_analysis.DataLoader')
    mock_loader.return_value.load_data.return_value = mock_data
    
    mock_cleaner = mocker.patch('run_analysis.DataCleaner')
    mock_cleaner.return_value.clean_data.return_value = mock_data

    mock_calculator = mocker.patch('run_analysis.FactorCalculator')
    mock_calculator.return_value.calculate_momentum.return_value = mock_data
    mock_calculator.return_value.calculate_volatility.return_value = mock_data

    mock_constructor = mocker.patch('run_analysis.PortfolioConstructor')
    mock_constructor.return_value.construct_portfolio.return_value = {'stock_a': 0.5, 'stock_b': 0.5}

    mock_balancer = mocker.patch('run_analysis.PortfolioBalancer')
    mock_balancer.return_value.balance_portfolio.return_value = {'stock_a': 0.5, 'stock_b': 0.5}

    # Run the test
    result = run_analysis('exposure_trade.csv')
    print(result)
    assert result == {'price': 0.1}