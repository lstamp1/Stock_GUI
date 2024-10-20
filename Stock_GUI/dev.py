# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 14:56:36 2024

@author: liams
"""

import yfinance as yf
import matplotlib.pyplot as plt

# Define the stock symbol (e.g., AAPL for Apple)
ticker = 'AAPL'

# Get the stock's financial data
stock = yf.Ticker(ticker)

# Get the income statement (quarterly data by default)
income_statement = stock.financials.T  # Transpose to get dates as rows

# Select revenue and profit columns
revenue = income_statement['Total Revenue']
profit = income_statement['Net Income']

# Convert revenue and profit to billions for better readability
revenue_billion = revenue / 10**9
profit_billion = profit / 10**9

# Plotting Year-over-Year Revenue and Profit
plt.figure(figsize=(10, 6))
plt.plot(revenue_billion.index, revenue_billion, label='Revenue (in Billion $)', marker='o')
plt.plot(profit_billion.index, profit_billion, label='Net Profit (in Billion $)', marker='o')

# Add labels, title, and legend
plt.xlabel('Year')
plt.ylabel('Amount (Billion $)')
plt.title(f"{ticker} Revenue and Profit Over Time")
plt.legend()

# Show the plot
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()


