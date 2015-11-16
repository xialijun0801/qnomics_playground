
# coding: utf-8

# In[253]:

import pandas as pd
equityDataSmall = "data/sp500_data_small.csv"
fundamentalDataSmall = "data/sp500_fundamental_small_s.csv"


# In[254]:

from datetime import datetime
dtypes = [str, datetime, float] 
fields = ['Ticker', 'Date', 'AClose']
equityPrice = pd.read_csv(equityDataSmall, usecols= [0, 1, 12], names = fields)
equityPrice.index = equityPrice['Ticker']


# In[663]:

fields = ['Ticker', 'Field', 'Frequency', 'Date', 'Value']
equityFundamental = pd.read_csv(fundamentalDataSmall, skiprows = 1, names = fields, parse_dates=True)
equityFundamental.index = equityFundamental['Ticker']
equityShares = equityFundamental[equityFundamental['Field'] == 'SHARESWA']


# In[664]:

tickers1 = set(equityPrice['Ticker'].unique())
tickers2 = set(equityShares['Ticker'].unique())
commonTickers_list = list(tickers1 & tickers2)


# In[669]:

commonTickers = pd.DataFrame(commonTickers_list)


# In[670]:

commonTickers.columns = ['Ticker']
commonTickers.index = commonTickers['Ticker']


# In[671]:

equityPrice_1 = pd.merge(equityPrice, commonTickers, how = 'inner', left_index = True, right_index = True)


# In[672]:

equityShares_1 = pd.merge(equityShares,commonTickers, how = 'inner', left_index = True, right_index = True)


# In[673]:

equityShares_1.index = pd.to_datetime(equityShares_1['Date'])
equityPrice_1.index = pd.to_datetime(equityPrice_1['Date'])


# In[684]:

equityShares_2 = equityShares_1[equityShares_1['Date'] > '2004-01-01']
equityShares_2 = equityShares_2[equityShares_2['Date'] < '2015-01-01']
equityPrice_2 = equityPrice_1[equityPrice_1['Date'] > '2005-01-01']
equityPrice_2 = equityPrice_2[equityPrice_2['Date'] < '2015-01-01']


# In[685]:

equityShares_3 = equityShares_2[equityShares_2['Frequency'] == 'MRQ']


# In[686]:

equityShares_4 = pd.DataFrame(columns = ['Ticker', 'Shares'])
for ticker in commonTickers_list:
    temp = equityShares_3[equityShares_3['Ticker_x'] == ticker]
    if (len(temp) > 0):
        temp = temp.resample('B', fill_method = 'ffill')[['Value']]
        temp['Ticker'] = ticker
        temp.columns = ['Shares', 'Ticker']
        equityShares_4 = pd.concat([equityShares_4, temp])


# In[693]:

equityPrice_2 = equityPrice_2[['Ticker_x', 'AClose']]
equityPrice_2.columns = ['Ticker','AClose']


# In[677]:

equityPrice_2_trans = equityPrice_2.reset_index().rename(columns = {0: 'Date'}).pivot('Date', 'Ticker', 'AClose')


# In[678]:

equityPrice_2_trans = equityPrice_2_trans.fillna(0) 


# In[680]:

equityShares_4_trans = equityShares_4.reset_index().rename(columns = {'index': 'Date'}).pivot('Date', 'Ticker', 'Shares')


# In[681]:

equityShares_4_trans = equityShares_4_trans.fillna(0)


# In[705]:

multiply_result = equityPrice_2_trans.multiply(equityShares_4_trans, axis=0, level=None, fill_value=0)
import numpy as np
mask = np.all(np.isnan(multiply_result) | np.equal(multiply_result, 0), axis=1)
multiply_result = multiply_result[~mask]


# In[706]:

add_result = multiply_result.cumsum(axis = 1)


# In[752]:

MV = add_result.ix[:, -1]
MV.columns = ['Past']


# In[743]:

multiply_result_2 = equityPrice_2_trans.shift(1).multiply(equityShares_4_trans, axis=0, level=None, fill_value=0)
import numpy as np
mask = np.all(np.isnan(multiply_result_2) | np.equal(multiply_result_2, 0), axis=1)
multiply_result_2 = multiply_result_2[~mask]
add_result_2 = multiply_result_2.cumsum(axis = 1)
MV_2 = add_result_2.ix[:, -1]
MV_2.columns = ['Now']


# In[740]:

merge = pd.concat([MV.shift(1), MV_2], axis =1)


# In[770]:

divisor = MV.shift(1).div(MV_2)


# In[771]:

MV_adjusted = MV.multiply(divisor)


# In[774]:

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
MV_adjusted.plot()


# In[775]:

#use daily return to calculate annualized volatility and Sharpe ratio on the rolling 12M basis over the past 5 years.
daily_rets = MV_adjusted.pct_change()


# In[780]:

data_mean = pd.rolling_mean(daily_rets,window = 252) 
data_std = pd.rolling_std(daily_rets, window = 252)
sr = data_mean.div(data_std)*np.sqrt(252)


# In[781]:

sr.plot()


# In[788]:

data_max = pd.rolling_max(MV_adjusted,window = 252) 
data_min = pd.rolling_min(MV_adjusted, window = 252)


# In[789]:

diff = data_max- data_min


# In[790]:

max_drawdown = diff.div(data_max)


# In[791]:

max_drawdown.plot()


# In[ ]:



