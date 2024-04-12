import pandas as pd
from factor_investment.portfolio_constructor import PortfolioConstructor
import pytest

def test_empty_asset_list():
    """Test that the constructor raises an error if asset list is empty."""
    constructor = PortfolioConstructor([])
    with pytest.raises(ValueError):
        constructor.construct_custom_weight()

def test_non_empty_portfolio():
    """Test the portfolio is not empty after construction."""
    assets = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
    weight = 1 / len(assets)
    asset_weights = {asset: weight for asset in assets}
    constructor = PortfolioConstructor(assets)
    portfolio = constructor.construct_custom_weight(asset_weights)
    assert len(portfolio) > 0, "Portfolio should not be empty."

