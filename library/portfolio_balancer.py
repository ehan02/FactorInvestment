from abc import ABC, abstractmethod

class PortfolioBalancer:
    def __init__(self, frequency='daily'):
        """ Initialize the PortfolioBalancer with a specified frequency ('daily' or 'monthly'). """
        self.frequency = frequency

    def rebalance_portfolio(self, current_positions, target_weights):
        """ Template method that defines the sequence of steps to rebalance the portfolio. """
        self.current_positions = current_positions
        self.target_weights = target_weights

        self.validate_inputs()
        self.calculate_required_trades()
        self.execute_trades()

    def validate_inputs(self):
        """ Validate the inputs to ensure they are correct and sufficient for the rebalancing process. """
        assert sum(self.target_weights.values()) == 1, "Target weights must sum to 1"
        assert all(asset in self.current_positions for asset in self.target_weights), "All target assets must be in current positions"

    def calculate_required_trades(self):
        """ Calculate the trades needed to align the current portfolio with the target weights. """
        total_value = sum(self.current_positions.values())
        self.trades = {}
        for asset, weight in self.target_weights.items():
            target_value = total_value * weight
            current_value = self.current_positions[asset]
            self.trades[asset] = target_value - current_value

    def execute_trades(self):
        """ Execute the trades calculated in the previous step based on the specified frequency. """
        print(f"{self.frequency.capitalize()} Balancer executing trades:")
        for asset, trade in self.trades.items():
            print(f"Trade for {asset}: Adjust by {trade:.2f}")
