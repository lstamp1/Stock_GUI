# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 16:18:34 2024

@author: liams
"""

import yfinance as yf
from datetime import datetime, timedelta

def yf_Dataframe(ticker, days_of_data):
    """
    Example: yf_Dataframe('PLTR', 10)
    
    Parameters
    ----------
    ticker : STRING
        Enter ticker in all Caps as a string
    start_time_days_ago : INT
        Days prior to today. Does not include the non-market 
        days and will return less than the specified INT. 

    Returns
    -------
    ticker_data : DataFrame
        DataFrame includes Open, High, Low, Close, Adj Close, and Volume. 

    """
    

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days = days_of_data)).strftime('%Y-%m-%d')
    ticker_data = yf.download(ticker,start = start_date, end = end_date)
    return ticker_data



def yf_Dataframe2(ticker, start_date, end_date):
    """
    Example: yf_Dataframe('PLTR', 10)
    
    Parameters
    ----------
    ticker : STRING
        Enter ticker in all Caps as a string
    start_time_days_ago : INT
        Days prior to today. Does not include the non-market 
        days and will return less than the specified INT. 

    Returns
    -------
    ticker_data : DataFrame
        DataFrame includes Open, High, Low, Close, Adj Close, and Volume. 

    """
    
    date_format = "%m/%d/%y"
    
    # Convert the start and end date strings to datetime objects
    start_date = datetime.strptime(start_date, date_format).strftime('%Y-%m-%d')
    end_date = datetime.strptime(end_date, date_format).strftime('%Y-%m-%d')
    
    # Download ticker data from yfinance
    ticker_data = yf.download(ticker, start=start_date, end=end_date)
    return ticker_data


