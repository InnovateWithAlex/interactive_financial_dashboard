# data_fetch.py

import yfinance as yf
import pandas as pd

def fetch_data(symbols=["SPY", "QQQ"], start_date="2024-01-01", end_date="2024-11-08"):
    # Fetch data
    data = yf.download(symbols, start=start_date, end=end_date, group_by='ticker')
    return data

# If you want to allow import to work seamlessly, add the following line
__all__ = ["fetch_data"]
