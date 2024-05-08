from library.data_loader import DataLoader
from library.data_cleaner import ConvertToFloatStrategy,FillMissingDataStrategy, WinsorizationStrategy, DataCleaner
from library.factor_calculator import PEFactorCalculator, PBFactorCalculator, EVToEBITDAFactorCalculator
from library.portfolio_constructor import PortfolioConstructor
from library.portfolio_balancer import PortfolioBalancer
import pandas as pd

def run_analysis():
    # Load Data
    loader = DataLoader('csv', 'tests/stock_data.csv')
    stock_data = loader.load_data()
  
    strategies = [ConvertToFloatStrategy(),FillMissingDataStrategy(), WinsorizationStrategy(0.05, 0.95)]    
    strategies = [ConvertToFloatStrategy()]    
    cleaner = DataCleaner(strategies)
    clean_data = cleaner.clean_data(stock_data.copy())
    
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
    # target_weights =  0
    # if len(factor_data) != 0:
    #     target_weights = 1 / len(factor_data)
    # # Example usage
    # current_positions = {'StockA': 100000, 'StockB': 150000}
    # target_weights = {'StockA': 0.5, 'StockB': 0.5}

    # # Create an instance for daily balancing
    # daily_balancer = PortfolioBalancer(frequency='daily')
    # daily_balancer.rebalance_portfolio(current_positions, target_weights)

    # # Create an instance for monthly balancing
    # monthly_balancer = PortfolioBalancer(frequency='monthly')
    # monthly_balancer.rebalance_portfolio(current_positions, target_weights)

if __name__ == "__main__":
    # Example: replace 'path/to/data.csv' with the path to your data file
    result = run_analysis()
    
