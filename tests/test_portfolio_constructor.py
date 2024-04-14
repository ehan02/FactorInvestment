import pytest
import numpy as np
from pathlib import Path
from factor_investment.portfolio_constructor import PortfolioBuilder
from factor_investment.investment_strategy import InvestmentStrategy

base_path = Path(__file__).parent
test_config = base_path /  'test_config.json'

# Mock strategy classes for testing
class MockStrategy(InvestmentStrategy):
    def apply_strategy(self, weights, factors):
        return np.sum(weights * factors['constant_factor'])  # Simplified strategy for testing

@pytest.fixture
def mock_factors():
    # Sample factors data for testing
    return {
        'constant_factor': np.array([1.0, 1.0, 1.0, 1.0, 1.0])
    }

@pytest.fixture
def initial_weights():
    # Initial weights, equally distributed
    return np.array([0.2, 0.2, 0.2, 0.2, 0.2])

@pytest.fixture
def strategies():
    # Setup strategies
    return [MockStrategy()]

def test_load_constraints(strategies):
    # Test loading of constraints from a configuration file
    builder = PortfolioBuilder(strategies, test_config)
    assert builder.constraints['min_weight'] == 0.01
    assert builder.constraints['max_weight'] == 0.25
    assert builder.constraints['total_investment'] == 1.0

def test_portfolio_optimization(strategies, initial_weights, mock_factors):
    # Test the portfolio optimization logic
    builder = PortfolioBuilder(strategies, test_config)
    optimized_weights = builder.build(initial_weights, mock_factors)
    assert len(optimized_weights) == 5
    assert np.isclose(np.sum(optimized_weights), 1.0)  # Ensure total investment constraint is met
    assert all(0.01 <= w <= 0.25 for w in optimized_weights)  # Check if individual weight constraints are met

# The above tests assume the existence of 'test_config.json' with appropriate content.
