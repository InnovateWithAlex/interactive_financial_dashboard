import pandas as pd
import plotly.graph_objects as go
from data.data_fetch import fetch_data
from calculations.financial_calculations import (
    calculate_rsi,
    calculate_macd,
    calculate_beta,
    calculate_volatility
)

# Fetch data for visualization
spy_data = fetch_data(symbols=["SPY", "QQQ"], start_date="2024-01-01", end_date="2024-11-08")

# Calculate the daily returns for SPY and QQQ
spy_returns = spy_data[("SPY", "Close")].pct_change()
qqq_returns = spy_data[("QQQ", "Close")].pct_change()

# Calculate the Beta value
beta_value = calculate_beta(spy_returns, qqq_returns)

# Calculate RSI for SPY and QQQ and add them to the data
spy_data[("SPY", "RSI")] = calculate_rsi(spy_data[("SPY", "Close")])
spy_data[("QQQ", "RSI")] = calculate_rsi(spy_data[("QQQ", "Close")])

# Calculate MACD for SPY and QQQ and add to the data
spy_data[("SPY", "MACD")], spy_data[("SPY", "Signal")] = calculate_macd(spy_data[("SPY", "Close")]).values.T
spy_data[("QQQ", "MACD")], spy_data[("QQQ", "Signal")] = calculate_macd(spy_data[("QQQ", "Close")]).values.T

# Calculate Volatility for SPY and QQQ and add them to the data
spy_data[("SPY", "Volatility")] = calculate_volatility(spy_data[("SPY", "Close")])
spy_data[("QQQ", "Volatility")] = calculate_volatility(spy_data[("QQQ", "Close")])

# Create RSI Chart
def create_rsi_chart(data):
    fig = go.Figure()
    
    # Add RSI for SPY
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["SPY", "RSI"],
        mode='lines',
        name='SPY RSI'
    ))
    
    # Add RSI for QQQ
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["QQQ", "RSI"],
        mode='lines',
        name='QQQ RSI'
    ))
    
    # Update layout
    fig.update_layout(
        title='RSI (Relative Strength Index) for SPY and QQQ',
        xaxis_title='Date',
        yaxis_title='RSI',
        template='plotly_dark'
    )
    
    return fig

# Create MACD Chart
def create_macd_chart(data):
    fig = go.Figure()
    
    # Add MACD and Signal for SPY
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["SPY", "MACD"],
        mode='lines',
        name='SPY MACD'
    ))
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["SPY", "Signal"],
        mode='lines',
        name='SPY Signal'
    ))
    
    # Add MACD and Signal for QQQ
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["QQQ", "MACD"],
        mode='lines',
        name='QQQ MACD'
    ))
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["QQQ", "Signal"],
        mode='lines',
        name='QQQ Signal'
    ))
    
    # Update layout
    fig.update_layout(
        title='MACD (Moving Average Convergence Divergence) for SPY and QQQ',
        xaxis_title='Date',
        yaxis_title='MACD Value',
        template='plotly_dark'
    )
    
    return fig

# Create Volatility Chart
def create_volatility_chart(data):
    fig = go.Figure()
    
    # Add Volatility for SPY
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["SPY", "Volatility"],
        mode='lines',
        name='SPY Volatility'
    ))
    
    # Add Volatility for QQQ
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["QQQ", "Volatility"],
        mode='lines',
        name='QQQ Volatility'
    ))
    
    # Update layout
    fig.update_layout(
        title='Volatility for SPY and QQQ',
        xaxis_title='Date',
        yaxis_title='Volatility (Standard Deviation)',
        template='plotly_dark'
    )
    
    return fig

# Display Beta Value
def display_beta():
    return f"The Beta of SPY relative to QQQ for the selected period is: {beta_value:.2f}"

# Generate Visualizations
if __name__ == "__main__":
    # RSI Chart
    rsi_chart = create_rsi_chart(spy_data)
    rsi_chart.show()
    
    # MACD Chart
    macd_chart = create_macd_chart(spy_data)
    macd_chart.show()
    
    # Volatility Chart
    volatility_chart = create_volatility_chart(spy_data)
    volatility_chart.show()
    
    # Display Beta Value
    print(display_beta())
