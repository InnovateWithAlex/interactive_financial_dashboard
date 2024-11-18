# calculations.py

import pandas as pd
import numpy as np
from data.data_fetch import fetch_data 

# Fetch data for calculations
spy_data = fetch_data(symbols=["SPY", "QQQ"], start_date="2024-01-01", end_date="2024-11-08")

# Calculate Relative Strength Index (RSI)
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Update the calculate_macd function
def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = data.ewm(span=short_window, adjust=False).mean()
    long_ema = data.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return pd.DataFrame({"MACD": macd, "Signal": signal})

# Calculate Beta (original individual beta calculation)
def calculate_beta(stock_returns, market_returns):
    return stock_returns.cov(market_returns) / market_returns.var()

# Add this function to calculate Beta on a monthly basis in calculations.py
def calculate_beta_monthly(data, ticker1="SPY", ticker2="QQQ"):
    # Calculate percentage change for both tickers if not already present
    data[(ticker1, "Pct Change")] = data[(ticker1, "Close")].pct_change() * 100
    data[(ticker2, "Pct Change")] = data[(ticker2, "Close")].pct_change() * 100

    # Resample monthly returns
    monthly_returns = data[(ticker1, "Pct Change")].resample('MS').sum().to_frame()
    monthly_returns[ticker2] = data[(ticker2, "Pct Change")].resample('MS').sum()
    monthly_returns.columns = [ticker1, ticker2]

    # Calculate beta
    beta_value = monthly_returns[ticker1].cov(monthly_returns[ticker2]) / monthly_returns[ticker2].var()
    return beta_value

# Calculate Volatility
def calculate_volatility(data, window=14):
    return data.pct_change().rolling(window).std() * np.sqrt(252)

# Test the functions on spy_data
spy_rsi = calculate_rsi(spy_data[("SPY", "Close")])
print("RSI for SPY:")
print(spy_rsi.dropna().head())

spy_macd = calculate_macd(spy_data[("SPY", "Close")])
print("\nMACD for SPY:")
print(spy_macd.dropna().head())

# Assuming SPY is the stock and QQQ is the market for daily beta calculation
spy_returns = spy_data[("SPY", "Close")].pct_change()
qqq_returns = spy_data[("QQQ", "Close")].pct_change()
spy_beta = calculate_beta(spy_returns, qqq_returns)
print(f"\nBeta of SPY relative to QQQ (daily calculation): {spy_beta:.2f}")

# Calculate monthly beta using the new function
spy_beta_monthly = calculate_beta_monthly(spy_data)
print(f"\nBeta of SPY relative to QQQ (monthly calculation): {spy_beta_monthly:.2f}")

spy_volatility = calculate_volatility(spy_data[("SPY", "Close")])
print("\nVolatility for SPY:")
print(spy_volatility.dropna().head())
