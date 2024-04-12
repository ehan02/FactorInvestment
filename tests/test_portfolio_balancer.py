import pytest
from factor_investment.portfolio_balancer import PortfolioBalancer

def test_balance_portfolio():
    portfolio = {'stock_a': 500, 'stock_b': 300, 'stock_c': 200}
    balancer = PortfolioBalancer(portfolio)
    balanced = balancer.balance_portfolio()
    expected_balance = {'stock_a': 0.5, 'stock_b': 0.3, 'stock_c': 0.2}
    assert balanced == expected_balance
