import numpy as np
import json

class InvestmentStrategy:
    """Abstract base class for investment strategies."""
    def apply_strategy(self, weights, factors):
        raise NotImplementedError("Strategy must implement the apply_strategy method.")

class ValueStrategy(InvestmentStrategy):
    def apply_strategy(self, weights, factors):
        """Applies a value investing strategy based on Earnings per Share and Market Price."""
        pe_ratios = factors['MarketPrice'] / factors['EarningsPerShare']
        value_scores = 1 / pe_ratios
        return weights.dot(value_scores)

class MomentumStrategy(InvestmentStrategy):
    def apply_strategy(self, weights, factors):
        """Applies a momentum investing strategy based on EBITDA growth."""
        ebitda_growth = factors['EBITDA'].pct_change().fillna(0)
        return weights.dot(ebitda_growth)

class ValueMomentumCombinedStrategy(InvestmentStrategy):
    def apply_strategy(self, weights, factors):
        """Combines value and momentum strategies."""
        pe_ratios = factors['MarketPrice'] / factors['EarningsPerShare']
        value_scores = 1 / pe_ratios
        ebitda_growth = factors['EBITDA'].pct_change().fillna(0)
        combined_scores = value_scores + ebitda_growth
        return weights.dot(combined_scores)
