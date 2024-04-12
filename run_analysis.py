from factor_investment.data_loader import DataLoader
from factor_investment.data_cleaner import DataCleaner
from factor_investment.factor_calculator import FactorCalculator
from factor_investment.portfolio_constructor import PortfolioConstructor
from factor_investment.portfolio_balancer import PortfolioBalancer
import pandas as pd

def run_analysis(file_path):
    # Load Data
    loader = DataLoader('csv', file_path)
    data = loader.load_data()

    # Clean Data
    cleaner = DataCleaner(data)
    clean_data = cleaner.clean_data()

    # Calculate Factors
    calculator = FactorCalculator(clean_data)
    factor_data = calculator.calculate_momentum()
    factor_data = calculator.calculate_volatility()

    # Construct Portfolio
    # constructor = PortfolioConstructor(factor_data)
    # portfolio = constructor.construct_portfolio()

    # # Balance Portfolio
    # balancer = PortfolioBalancer(portfolio)
    # balanced_portfolio = balancer.balance_portfolio()
    weight = 1 / len(factor_data)
    balanced_portfolio = {factor: weight for factor in factor_data}
    return balanced_portfolio

if __name__ == "__main__":
    # Example: replace 'path/to/data.csv' with the path to your data file
    result = run_analysis('tests/exposure_trade.csv')
    print(result)
