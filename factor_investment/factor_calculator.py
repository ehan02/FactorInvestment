from abc import ABC, abstractmethod
import pandas as pd

class BaseFactorCalculator(ABC):
    def __init__(self, data):
        self.data = data

    def calculate_factors(self):
        self.preprocess_data()
        result = self.compute_factor()
        result = self.postprocess_data(result)
        return result

    def preprocess_data(self):
        # Placeholder for any preprocessing needed
        pass

    @abstractmethod
    def compute_factor(self):
        pass

    def postprocess_data(self, result):
        # Placeholder for any postprocessing like normalization
        return result

class PEFactorCalculator(BaseFactorCalculator):
    def compute_factor(self):
        pe_ratio = self.data['MarketPrice'] / self.data['EarningsPerShare']
        return pe_ratio

class PBFactorCalculator(BaseFactorCalculator):
    def compute_factor(self):
        pb_ratio = self.data['MarketPrice'] / self.data['BookValuePerShare']
        return pb_ratio

class EVToEBITDAFactorCalculator(BaseFactorCalculator):
    def compute_factor(self):
        ev_to_ebitda = self.data['EnterpriseValue'] / self.data['EBITDA']
        return ev_to_ebitda

class MomentumFactorCalculator(BaseFactorCalculator):
    def compute_factor(self):
        momentum = self.data['EnterpriseValue'] / self.data['EBITDA']
        return momentum


class FactorScorer:
    def score_factors(self, factors):
        # Example: Normalize and score factors
        scored = (factors - factors.mean()) / factors.std()
        return scored.rank()

class OutputHandler:
    def format_output(self, scored_factors):
        # Example: Convert DataFrame to CSV or another format for output
        return scored_factors.to_csv()

def main():
    # Example usage
    # Load your data
    data = pd.DataFrame({
        'MarketPrice': [100, 200, 150],
        'EarningsPerShare': [5, 20, 5],
        'BookValuePerShare': [50, 100, 75],
        'EnterpriseValue': [1000, 2000, 1500],
        'EBITDA': [10, 200, 150]
    })
    
    pe_calculator = PEFactorCalculator(data)
    pb_calculator = PBFactorCalculator(data)
    ev_to_ebitda_calculator = EVToEBITDAFactorCalculator(data)

    # Calculate factors
    pe_ratio = pe_calculator.calculate_factors()
    pb_ratio = pb_calculator.calculate_factors()
    ev_to_ebitda = ev_to_ebitda_calculator.calculate_factors()

    # Combine all factors into a DataFrame
    factor_data = pd.DataFrame({
        'PE': pe_ratio,
        'PB': pb_ratio,
        'EVToEBITDA': ev_to_ebitda
    })

    print(factor_data)
    # Score factors
    scorer = FactorScorer()
    scored_factors = scorer.score_factors(factor_data)

    # Handle output
    output_handler = OutputHandler()
    formatted_output = output_handler.format_output(scored_factors)
    print(formatted_output)

if __name__ == "__main__": 
    main()
