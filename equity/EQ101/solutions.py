
# coding: utf-8
#*************************************************************************#
                                   #EQ101#
#*************************************************************************#

# In[2]:

import pandas as pd
equityDataSmall = "data/sp500_data_small.csv"
fundamentalDataSmall = "data/sp500_fundamental_small_s.csv"


# In[156]:

from datetime import datetime
dtypes = [str, datetime, float] 
fields = ['Ticker', 'Date', 'AOpen', 'AClose']
equityPrice = pd.read_csv(equityDataSmall, usecols= [0, 1, 11, 12], names = fields)
equityPrice.index = equityPrice['Ticker']


# In[157]:

fields = ['Ticker', 'Field', 'Frequency', 'Date', 'Value']
equityFundamental = pd.read_csv(fundamentalDataSmall, skiprows = 1, names = fields, parse_dates=True)
equityFundamental.index = equityFundamental['Ticker']
equityShares = equityFundamental[equityFundamental['Field'] == 'SHARESWA']


# In[158]:

tickers1 = set(equityPrice['Ticker'].unique())
tickers2 = set(equityShares['Ticker'].unique())
commonTickers_list = list(tickers1 & tickers2)


# In[159]:

#some tickers are not avaiable in the fundamental data, so only choose the ones are present
commonTickers = pd.DataFrame(commonTickers_list)
commonTickers.columns = ['Ticker']
commonTickers.index = commonTickers['Ticker']


# In[160]:

equityPrice_1 = pd.merge(equityPrice, commonTickers, how = 'inner', left_index = True, right_index = True)
equityShares_1 = pd.merge(equityShares,commonTickers, how = 'inner', left_index = True, right_index = True)


# In[161]:

equityShares_1.index = pd.to_datetime(equityShares_1['Date'])
equityPrice_1.index = pd.to_datetime(equityPrice_1['Date'])


# In[176]:

equityShares_2 = equityShares_1[(equityShares_1['Date'] > '2004-01-01') 
                                & (equityShares_1['Date'] < '2015-01-01')
                                & (equityShares_1['Frequency'] == 'MRQ')]
equityPrice_2 = equityPrice_1[ (equityPrice_1['Date'] > '2005-01-01')
                              & (equityPrice_1['Date'] < '2015-01-01')]


# In[163]:

equityShares_adjusted = pd.DataFrame(columns = ['Ticker', 'Shares'])
for ticker in commonTickers_list:
    temp = equityShares_2[equityShares_2['Ticker_x'] == ticker]
    if (len(temp) > 0):
        temp = temp.resample('B', fill_method = 'ffill')[['Value']]
        temp['Ticker'] = ticker
        temp.columns = ['Shares', 'Ticker']
        equityShares_adjusted = pd.concat([equityShares_adjusted, temp])


# In[177]:

equityPrice_2 = equityPrice_2[['Ticker_x', 'AOpen', 'AClose']]
equityPrice_2.columns = ['Ticker', 'AOpen', 'AClose']


# In[180]:

equityPrice_trans = equityPrice_2.reset_index().rename(columns = {0: 'Date'}).pivot('Date', 'Ticker', 'AClose').fillna(0)
#the equity price at open
equityPrice_open_trans = equityPrice_2.reset_index().rename(columns = {0: 'Date'}).pivot('Date', 'Ticker', 'AOpen').fillna(0)
equityShares_trans = equityShares_adjusted.reset_index().rename(columns = {'index': 'Date'}).pivot('Date', 'Ticker', 'Shares').fillna(0)


# In[181]:

totalMarketValue_each = equityPrice_trans.multiply(equityShares_trans, axis=0, level=None, fill_value=0)
#market value at open time
totalMarketValue_open_each = equityPrice_open_trans.multiply(equityShares_trans, axis=0, level=None, fill_value=0)
import numpy as np
mask = np.all(np.isnan(totalMarketValue_each) | np.equal(totalMarketValue_each, 0), axis=1)
totalMarketValue_each= totalMarketValue_each[~mask]
totalMarketValue_open_each= totalMarketValue_open_each[~mask]


# In[167]:

#pick the top 500
# the question here is how to reselect the top 500, it does not make sense to pick up the top 500 each day, 
# it does not make sense to keep using the same set of stock either
# shoud reselect at certain time interval
totalMarketValueMean = totalMarketValue_each.mean(axis = 0)
totalMarketValueMean = pd.DataFrame(totalMarketValueMean)
top500Security = list(totalMarketValueMean.sort().ix[0:499, ].index)


#bonus question pick the mid 500 - 10000

# In[168]:

totalMarketValueMean.columns = ['Mean'] 
midSecurity = list(totalMarketValueMean[(totalMarketValueMean['Mean'] < 1000e+06)
                                  & (totalMarketValueMean['Mean'] > 500e+06)].index) # 500 to 1000 million


# In[183]:

top500MarketValue_each = totalMarketValue_each[top500Security]
midMarketValue_each = totalMarketValue_each[midSecurity]
#the market value at open time
top500MarketValue_open_each = totalMarketValue_each[top500Security]
midMarketValue_open_each = totalMarketValue_each[midSecurity]


# In[201]:

top500TotalMarketValue = top500MarketValue_each.cumsum(axis = 1).ix[:, -1]
midTotalMarketValue = midMarketValue_each.cumsum(axis = 1).ix[:, -1]
top500TotalMarketValue_open = top500MarketValue_open_each.cumsum(axis = 1).ix[:, -1]
midTotalMarketValue_open = midMarketValue_open_each.cumsum(axis = 1).ix[:, -1]


# In[205]:

# to compare with the open market value of today with close market value of yesterday, which must be equal
top500TotalMarketValue_past = top500TotalMarketValue.shift(1)
top500TotalMarketValue_past.columns = ['Past']
midTotalMarketValue_past = midTotalMarketValue.shift(1)
midTotalMarketValue_past.columns = ['Past']


# In[209]:

top500Divisor = top500TotalMarketValue.div(top500TotalMarketValue_past)
midDivisor = top500TotalMarketValue.div(top500TotalMarketValue_past)


# In[252]:

top500Index_adjusted = top500TotalMarketValue.div(top500Divisor)[:-3]/top500TotalMarketValue[0]* 100
midIndex_adjusted = midTotalMarketValue.div(midDivisor)[:-3]/midTotalMarketValue[0] * 100
compare = top500Index_adjusted/midIndex_adjusted 


# In[260]:

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
plt.figure(1)

plt.subplot(311)
plt.plot(top500Index_adjusted)
plt.subplot(312)
plt.plot(midIndex_adjusted )

plt.subplot(313)
plt.plot(compare)


# In[233]:

#use daily return to calculate annualized volatility and Sharpe ratio on the rolling 12M basis over the past 5 years.
top500_daily_rets = top500Index_adjusted.pct_change()
mid_daily_rets = midIndex_adjusted.pct_change() 


# In[234]:

top500_data_mean = pd.rolling_mean(top500_daily_rets,window = 252) 
top500_data_std = pd.rolling_std(top500_daily_rets, window = 252)
top500_sr = top500_data_mean.div(top500_daily_rets)*np.sqrt(252)

mid_data_mean = pd.rolling_mean(mid_daily_rets,window = 252) 
mid_data_std = pd.rolling_std(mid_daily_rets, window = 252)
mid_sr = mid_data_mean.div(mid_daily_rets)*np.sqrt(252)


# In[239]:

top500_max = pd.rolling_max(top500Index_adjusted,window = 252) 
top500_min = pd.rolling_min(top500Index_adjusted, window = 252)

midIndex_max = pd.rolling_max(midIndex_adjusted,window = 252) 
midIndex_min = pd.rolling_min(midIndex_adjusted, window = 252)


# In[261]:

top500_diff = top500_max- top500_min
top500_max_drawdown = top500_diff.div(top500_max)
midIndex_diff = midIndex_max- midIndex_min
midIndex_max_drawdown = midIndex_diff.div(midIndex_max)


# In[241]:

top500_max_drawdown.plot()


# In[262]:

midIndex_max_drawdown.plot()


#*************************************************************************#
                                   #EQ102#
#*************************************************************************


#calcualte the earnings for one year
top500_year_earn = top500Index_adjusted.diff(252)
top500_year_earn.columns = ['Return']


# In[132]:

#get CPI value, and adjusted them by CPI
from datetime import datetime
dtypes = [datetime, float] 
fields = ['Date', 'CPI']
cpi = pd.read_csv("data/usa_cpi.csv", names = fields, skiprows= 1)
cpi.index = pd.to_datetime(cpi['Date'])
cpi = cpi['CPI']
cpi = cpi.asfreq('B', method = 'ffill')

#calculate the cpi change for one year +1
cpi_divisor = cpi.pct_change(252) + 1


# In[133]:

top500_year_earn_cpi = pd.concat([cpi_divisor, top500_year_earn], axis=1, join='inner')


# In[134]:

top500_year_earn_cpi.columns = ['CPI_divisor', 'Earning']
top500_year_earn_cpi['CPI_Adjusted_Earning'] = top500_year_earn_cpi['Earning'] / top500_year_earn_cpi['CPI_divisor']


# In[140]:

#moving average
# for Robert Shiller's Cyclically Adjusted PE Ratio it is using 10 year moving average
# for this one I try one year moving average
top500_year_earn_ma_10 = pd.rolling_mean(top500_year_earn, 2520, min_periods=1)
top500_year_earn_ma = pd.rolling_mean(top500_year_earn, 252, min_periods=1)


# In[141]:

top500_ep = 1/(top500Index_adjusted.div(top500_year_earn_ma))
top500_ep_cape = 1/(top500Index_adjusted.div(top500_year_earn_ma_10))


# In[142]:

top500_pe = pd.DataFrame(1/top500_ep)
top500_pe_cape = pd.DataFrame(1/top500_ep_cape)


# In[143]:

#using moving average return
top500_pe.columns = ['PE']
top500_pe[(top500_pe['PE'] < 0) 
          | (top500_pe['PE'] > 50) ] = None
top500_pe.plot()


# In[144]:

top500_pe_cape.plot()

