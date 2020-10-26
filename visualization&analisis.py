import pyfolio as pyf
import pandas as pd
import yfinance as yf

#tickers to analyze
tickers = ['AAPL','MSFT','AMZN','WMT']

#create a dataframe placeholder
data = pd.DataFrame(columns=tickers)

#get data
for ticker in tickers:
    data[ticker] = yf.download(ticker,period='5y',)['Adj Close']

#print(data.head())

# compute daily mean returns.
# The mean return is the daily portfolio returns with the above four stocks.
data = data.pct_change().dropna().mean(axis=1)
print(data.head())

pyf.create_full_tear_sheet(data)