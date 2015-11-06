EQ201 Smart Beta Indexes - Low Volatility
-------------------------

### Background

Low volatility anomaly was a very hot topic in and before 2014.  People argued
that low volatility stocks, though safer, on aggregate delivers higher returns
than high volatility stocks. Thus born many low volatility ETF such as `SPLV`
and `USMV`.

Low volatility strategy is one type of
[Smart Beta strategies](http://www.investopedia.com/terms/s/smart-beta.asp).

### Problem Description

Construct a `TOP500LV Index` (low volatility) and a `TOP500HV Index` (high
volatility) index for the US market according to the following rules:

0. the parent index is the `TOP500 Index` defined in `EQ101`
0. the index level represent an equal weighted portfolio of the 100 stocks in
   the candidate universe with the lowest (highest) past 252-day volatility.
0. the index is rebalanced on the close of the last business day of each month.
0. make sure the index level is not affected by corporate events (such as
   dividends, shares buybacks, M&A, de-listing, etc) that result in abrupt
   change of the stock's market cap.

### Questions

0. use daily returns to calculate annualized volatility and Sharpe ratio of
   `TOP500LV Index` on the rolling 12M basis over the past 5 years.
0. calculate the maximum draw downing of the index level for the past 5 years.
0. compare performance for all three indexes, `TOP500 Index`, `TOP500LV Index`,
   and `TOP500HV Index`.

### Bonus Questions

Another term 'Risk-on/Risk-off' has been frequently mentioned in recent years. It is
argued that when investors are turning from more risk-seeking to more
risk-averse, they dump risky asset (high volatility stocks) to buy safe assets
(low volatility stocks). Let's test such hypothesis.

0. Calculate the performance of a long/short strategy with 1 unit long position
   in `TOP500HV Index` and 1 unit short position in `TOP500LV Index`.
0. Compare the performance of the above strategy with `TOP500 Index`.  Can you
   draw some conclusion?

### Data

* [End of Day US Stock Prices](https://www.quandl.com/data/EOD)

### Reference

* Methodology - S&P 500 LOW VOLATILITY INDEX
* MSCI USA Minimum Volatility (USD) Index
