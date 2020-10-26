###
#   Script with examples about how to get data
###

#generic imports
import io
import json
import matplotlib.pyplot as plt 
#import matplotlib as plt
#%matplotlib inline
#pandas_datareader import
import pandas as pd
from pandas_datareader import data
#quandl
import quandl
from alpha_vantage import timeseries as avts
import yfinance as yf

start_date= '2015-01-01'
end_date = '2020-01-01'
tickers = ['AAPL','MSFT','IBM','WMT']

#getting secrets api key 
personaldatafile = open('personaldata.json','r')
json_keys = json.load(personaldatafile)
quandl_api_key = json_keys['quandl_api_key']
alpha_vantage_api_key = json_keys['alpha_vantage_api_key']
#----------------------------------------------------------------------
#padas_datareader
data_from_yahoo = data.get_data_yahoo(tickers[0],start_date,end_date)
print(data_from_yahoo.head())
#plot_data(data_to_plot = data_from_yahoo)
data_from_yahoo['Adj Close'].plot(figsize=(17,6))
plt.title('Adjusted close prices of %s from yahoo' % tickers[0],fontsize=16)
plt.ylabel('Price',fontsize=14)
plt.xlabel('Year',fontsize=14)
plt.grid(which='major',color='k',linestyle='-.',linewidth=0.5)
plt.show()
#----------------------------------------------------------------------

#get data
data_from_quandl = quandl.get('WIKI/'+tickers[0],start_date=start_date,end_date=end_date,api_key=quandl_api_key)
print(data_from_quandl.head())

#ploting
data_from_quandl['Adj. Close'].plot(figsize=(17,6))
plt.title('Adjusted close prices of %s from quandl' % tickers[0],fontsize=16)
plt.ylabel('Price',fontsize=14)
plt.xlabel('Year',fontsize=14)
plt.grid(color='k',linestyle='-.',linewidth=0.5)
plt.show()

#get multiples ticket data
data_multiples = pd.DataFrame(columns=tickers)
for ticket in tickers:
    data_multiples[ticket] = quandl.get('WIKI/'+ticket, start_date=start_date,end_date=end_date,api_key=quandl_api_key)['Adj. Close']

print(data_multiples.head())
data_multiples.plot(figsize=(17,6))
plt.title('Adjusted closes prices')
plt.ylabel('Price',fontsize=14)
plt.xlabel('Year',fontsize=14)
plt.grid(color='k',linestyle='-.',linewidth=0.5)
plt.show()

#----------------------------
#alpha vantage => get intraday data

ts = avts.TimeSeries(alpha_vantage_api_key,output_format='pandas')
data_intraday, data_intraday_info = ts.get_intraday(tickers[0],outputsize='full',interval='1min')
print(data_intraday_info)
print(data_intraday.head())

#get custome frecuency data
#During strategy modelling, you are required to work 
# with a custom frequency of stock market data such as 7 minutes or 35 minutes.
# This custom frequency candles are not provided by data vendors or web sources, but 
# you can always use pandas => 'resample'

#converting 1 min to 10 min frecuency sample data
# define dictionary for convention logic
ohlcv_dict = {
    '1. open':'first',
    '2. high':'max',
    '3. low':'min',
    '4. close':'last',
    '5. volume':'sum',
} 
#convert the dataframe index to datetime timestamp
data_intraday.index = pd.to_datetime(data_intraday.index)

#call resample method with desired frecuency
# .10T for 10 minutes,
# .D for 1 day and
# .M for 1 month
data_intraday_10min = data_intraday.resample('10T').agg(ohlcv_dict)
print(data_intraday.head())

#---------------------------------------------------------------------
#yfincance
# you can get up to 7 intray data

data = yf.download(tickers=tickers[0],period='5d',interval='1m')
print(data.head())

#funamentals data
msft = yf.Ticker(tickers[0])
# show income statement
print(msft.financials)
# show balance heet
msft.balance_sheet
# show cashflow
msft.cashflow
# show other info
msft.info

#price to book and price to earning ratio

pb = msft.info['priceToBook']
#pe = msft.info['regularMarketPrice']/msft.info['epsTrailingTwelveMonths'] # this had error, check for correct key dict


print('-- Fundamental Ratios---')
print('Price to book ratio is %.2f' % pb)
#print('Price to earning ratio is %2.f' % pe)

#show revenues
revenue = msft.financials.loc['TotalRevenue']
plt.bar(revenue.index, revenue.values)
plt.ylabel('Total Revenues')
plt.show()

#show earnings Before Interest and Taxes
ebit = msft.financials.loc['Earnings Before Interest and Taxes']
plt.bar(ebit.index, ebit.values)
plt.ylabel('EBIT')
plt.show()

#-----------------------------------------------------------------

# The (import nsepy) package is used to get the stock market data for the futures 
# and options for Indian stocks and indices.

#Future data 
# from datetime import date
# from nsepy import get_history
# # Stock options (for index options, set index = True)
# stock_fut = get_history(symbol="HDFC",
#  start=date(2019, 1, 15),
#  end=date(2019, 2, 1),
#  futures=True,
#  expiry_date=date(2019, 2, 28))
# stock_fut.head()

#Option data
# from datetime import date
# from nsepy import get_history
# stock_opt = get_history(symbol="HDFC",
#  start=date(2019, 1, 15),
#  end=date(2019, 2, 1),
#  option_type="CE",
#  strike_price=2000,
#  expiry_date=date(2019, 2, 28))
# stock_opt.head()