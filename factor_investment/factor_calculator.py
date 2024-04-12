class FactorCalculator:
    def __init__(self, data):
        self.data = data

    def calculate_momentum(self):
        """Calculates the momentum factor as the percentage change over a specified period."""
        self.data['momentum'] = self.data['price'].pct_change(periods=3)  # Calculating momentum over 3 days
        return self.data

    def calculate_volatility(self):
        """Calculates the volatility of the stock prices."""
        self.data['volatility'] = self.data['price'].rolling(window=10).std()
        return self.data
