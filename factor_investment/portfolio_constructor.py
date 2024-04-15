import numpy as np
from scipy.optimize import minimize
import json
from factor_investment.investment_strategy import ValueStrategy, MomentumStrategy, ValueMomentumCombinedStrategy

class PortfolioConstructor:
    def __init__(self, strategies, config_path='config.json'):
        self.strategies = strategies
        self.load_constraints(config_path)

    def load_constraints(self, config_path):
        """Load constraints from a JSON configuration file."""
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.constraints = config.get('constraints', {})

    def build(self, weights, factors):
        """Construct the portfolio based on the set constraints and strategies."""
        # Set bounds using min and max weight constraints from the configuration
        bounds = [(self.constraints.get('min_weight', 0.01), self.constraints.get('max_weight', 0.25)) for _ in range(len(weights))]
        constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - self.constraints.get('total_investment', 1)}]
        result = minimize(self.combined_objective, weights, args=(factors,), bounds=bounds, constraints=constraints)
        return result.x

    def combined_objective(self, weights, factors):
        """Combine returns from multiple strategies and manage risk."""
        total_return = sum(strategy.apply_strategy(weights, factors) for strategy in self.strategies)
        portfolio_risk = np.std(weights)
        risk_penalty = portfolio_risk ** 2
        return -(total_return - risk_penalty)

# Example of setting up the PortfolioBuilder with strategies
if __name__ == '__main__':
    strategies = [ValueStrategy(), MomentumStrategy(), ValueMomentumCombinedStrategy()]
    builder = PortfolioConstructor(strategies)
    # Example usage assuming 'weights' and 'factors' are predefined
    # factors = {'MarketPrice': ..., 'EarningsPerShare': ..., 'EBITDA': ...}
    # weights = np.array([...])
    # optimized_weights = builder.build(weights, factors)
    # print("Optimized Portfolio Weights:", optimized_weights)
