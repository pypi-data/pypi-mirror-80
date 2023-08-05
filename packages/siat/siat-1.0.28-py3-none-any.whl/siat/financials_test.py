# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 10:22:47 2020

@author: Peter
"""

import os; os.chdir("S:/siat")
from siat.financial_statements import *
fs_aapl=get_financial_rates('AAPL')

from siat.financials import *

rates=get_stock_profile('AAPL',info_type='fin_rates')

tickers=['AAPL','MSFT','WMT','FB','QCOM']
cr=compare_snapshot(tickers,'Current Ratio')
beta=compare_snapshot(tickers,'beta')
dtoe=compare_snapshot(tickers,'Debt to Equity')
dtoe=compare_snapshot(tickers,'?')
teps=compare_snapshot(tickers,'Trailing EPS')
tpe=compare_snapshot(tickers,'Trailing PE')

tickers1=['AMZN','EBAY','GRPN','BABA','JD','PDD','VIPS']
gm=compare_snapshot(tickers1,'Gross Margin')
pm=compare_snapshot(tickers1,'Profit Margin')

df1,df2=compare_history('AAPL','Current Ratio')
df1,df2=compare_history('AAPL',['Current Ratio','Quick Ratio'])
df1,df2=compare_history('AAPL',['BasicEPS','DilutedEPS'])
df1,df2=compare_history('AAPL',['Current Ratio','BasicEPS'],twinx=True)
df1,df2=compare_history('AAPL',['BasicPE','BasicEPS'])
df1,df2=compare_history('AAPL',['BasicPE','BasicEPS'],twinx=True)

df1,df2=compare_history(['AAPL','MSFT'],['BasicPE','BasicEPS'])
df1,df2=compare_history(['AAPL','MSFT'],['BasicPE','BasicEPS'],twinx=True)
df1,df2=compare_history(['AAPL','MSFT'],'BasicEPS',twinx=True)

cr=compare_history(['INTL','QCOM'],'Current Ratio',twinx=True)

cr=compare_history(['600519.SS','000002.SZ'],'Current Ratio',twinx=True)
