import pyfolio as pf

# Define the ticker list
tickers_list = ['AAPL', 'AMZN', 'MSFT', 'WMT']
# Import pandas and create a placeholder for the data
import pandas as pd
data = pd.DataFrame(columns=tickers_list)
# Feth the data
import yfinance as yf
for ticker in tickers_list:
 data[ticker] = yf.download(ticker, period='5y',)['Adj Close']
# Compute the returns of individula stocks and then compute the daily mean returns.
# The mean return is the daily portfolio returns with the above four stocks.
data = data.pct_change().dropna().mean(axis=1)
# Print first 5 rows of the data
print(data.head())

pf.create_full_tear_sheet(data)
