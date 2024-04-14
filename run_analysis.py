from factor_investment.data_loader import DataLoader
from factor_investment.data_cleaner import ConvertToFloatStrategy,FillMissingDataStrategy, WinsorizationStrategy, DataCleaner
from factor_investment.factor_calculator import PEFactorCalculator, PBFactorCalculator, EVToEBITDAFactorCalculator
from factor_investment.portfolio_constructor import PortfolioConstructor
from factor_investment.portfolio_balancer import PortfolioBalancer
import pandas as pd

def run_analysis(file_path):
    # Load Data
    loader = DataLoader('csv', file_path)
    data = loader.load_data()
   
  
    strategies = [ConvertToFloatStrategy(),FillMissingDataStrategy(), WinsorizationStrategy(0.05, 0.95)]    
    strategies = [ConvertToFloatStrategy()]    
    cleaner = DataCleaner(strategies)
    clean_data = cleaner.clean_data(data.copy())
    
    # Calculate Factors
    calculator = PEFactorCalculator(clean_data)    
    factor_data = calculator.calculate_factors()    
    print("factor data:")
    print(factor_data)

    # Construct Portfolio
    # constructor = PortfolioConstructor(factor_data)
    # portfolio = constructor.construct_portfolio()

    # # Balance Portfolio
    # balancer = PortfolioBalancer(portfolio)
    # balanced_portfolio = balancer.balance_portfolio()
    weight =  0
    if len(factor_data) != 0:
        weight = 1 / len(factor_data)
    balanced_portfolio = {factor: weight for factor in factor_data}
    return balanced_portfolio

if __name__ == "__main__":
    # Example: replace 'path/to/data.csv' with the path to your data file
    result = run_analysis('tests/exposure_trade.csv')
    
