class PortfolioBalancer:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def balance_portfolio(self):
        """Rebalances the portfolio by equalizing the weights of each asset."""
        total_value = sum(self.portfolio.values())
        for stock, value in self.portfolio.items():
            self.portfolio[stock] = value / total_value
        return self.portfolio
