import pytest
from library.portfolio_balancer import PortfolioBalancer

def test_validate_inputs():
    balancer = PortfolioBalancer('daily')
    positions = {'stock': 1000, 'bond': 500}
    
    # Test case where sum of weights is not 1
    with pytest.raises(AssertionError):
        balancer.rebalance_portfolio(positions, {'stock': 0.6, 'bond': 0.5})
    
    # Test case where an asset is missing
    with pytest.raises(AssertionError):
        balancer.rebalance_portfolio({'stock': 1000}, {'stock': 0.6, 'bond': 0.4})

