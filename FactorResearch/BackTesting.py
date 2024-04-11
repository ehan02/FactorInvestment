import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import statsmodels.api as sm


def calculate_beta(stock_returns, market_returns):
    """Calculate beta of stocks based on market returns."""
    stock_returns = stock_returns.dropna()
    market_returns = market_returns.dropna()
    X = sm.add_constant(market_returns)  # Adds a constant term to the predictor
    model = sm.OLS(stock_returns, X).fit()
    return model.params[1]

def calculate_factors(stock_data, market_symbol):
    """Calculate beta, value (P/E ratio), and momentum factors."""
    market_returns = stock_data[market_symbol].pct_change()
    factors = pd.DataFrame(index=stock_data.columns)
    
    for symbol in stock_data.columns:
        if symbol == market_symbol:
            continue
        stock_returns = stock_data[symbol].pct_change()
        factors.loc[symbol, 'Beta'] = calculate_beta(stock_returns, market_returns)
        stock_info = yf.Ticker(symbol).info
        factors.loc[symbol, 'PE_Ratio'] = stock_info.get('forwardPE', np.nan)
        factors.loc[symbol, 'Momentum'] = stock_data[symbol].pct_change(periods=120).iloc[-1]  # 6-month momentum
    
    factors['Value'] = 1 / factors['PE_Ratio']  # Inverse of P/E ratio for value
    return factors.dropna()

def select_stocks(factors, top_n=10):
    """Select top N stocks based on factors."""
    # Normalize factors
    print(top_n)
    factors['Beta_Score'] = 1 - (factors['Beta'] - factors['Beta'].min()) / (factors['Beta'].max() - factors['Beta'].min())
    factors['Value_Score'] = (factors['Value'] - factors['Value'].min()) / (factors['Value'].max() - factors['Value'].min())
    factors['Momentum_Score'] = (factors['Momentum'] - factors['Momentum'].min()) / (factors['Momentum'].max() - factors['Momentum'].min())
    
    # Composite score
    factors['Composite_Score'] = factors[['Beta_Score', 'Value_Score', 'Momentum_Score']].mean(axis=1)
    
    # Select top N stocks
    selected_stocks = factors.nlargest(top_n, 'Composite_Score')
    return selected_stocks.index.tolist()

def calculate_performance_metrics(returns, risk_free_rate=0.01):
    """
    Calculate Sharpe Ratio, Maximum Drawdown, and Annualized Volatility.

    returns: Daily returns of the portfolio
    risk_free_rate: Risk-free rate, default is 1% (0.01) annually
    """
    # Convert annual risk-free rate to daily
    daily_risk_free_rate = np.power(1 + risk_free_rate, 1/252) - 1

    # Sharpe Ratio
    excess_returns = returns - daily_risk_free_rate
    sharpe_ratio = np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns)

    # Maximum Drawdown
    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()

    # Annualized Volatility
    volatility = np.std(returns) * np.sqrt(252)

    return sharpe_ratio, max_drawdown, volatility

def backtest_strategy(symbols, start_date, end_date, rebalance_period='1M'):
    data = yf.download(symbols, start=start_date, end=end_date)['Adj Close']
    market_returns = data['^GSPC'].resample(rebalance_period).ffill().pct_change()[1:]
    
    portfolio_returns = []
    start_period = pd.to_datetime(start_date)
    end_period = pd.to_datetime(end_date)
    current_date = start_period

    while current_date < end_period:
        next_rebalance_date = (current_date + pd.DateOffset(months=1)).replace(day=1)
        period_data = data.loc[current_date:min(next_rebalance_date, end_period)]
        factors = calculate_factors(period_data, '^GSPC')
        selected_stocks = select_stocks(factors)
        
        next_period_data = data.loc[next_rebalance_date:min(next_rebalance_date + pd.DateOffset(months=1), end_period), selected_stocks]
        next_period_returns = next_period_data.pct_change().mean(axis=1)[1:]
        
        portfolio_returns.extend(next_period_returns.tolist())
        current_date = next_rebalance_date
    
    portfolio_returns = np.array(portfolio_returns)
    portfolio_cumulative_returns = np.cumprod(1 + portfolio_returns) - 1
    market_cumulative_returns = np.cumprod(1 + market_returns) - 1

    # Plot cumulative returns
    # plt.figure(figsize=(14, 7))
    # plt.plot(market_cumulative_returns.index, market_cumulative_returns, label='Market')
    # plt.plot(market_cumulative_returns.index, portfolio_cumulative_returns, label='Portfolio', linestyle='--')
    # plt.title('Backtest Results')
    # plt.xlabel('Date')
    # plt.ylabel('Cumulative Returns')
    # plt.legend()
    # plt.show()

    # Calculate and display performance metrics
    sharpe_ratio, max_drawdown, volatility = calculate_performance_metrics(portfolio_returns)
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Maximum Drawdown: {max_drawdown:.2f}")
    print(f"Annualized Volatility: {volatility:.2f}")

if __name__ == '__main__':
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', '^GSPC']
    start_date = '2019-01-01'
    end_date = '2021-01-01'
    
    backtest_strategy(symbols, start_date, end_date)
