# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 21:44:13 2023

@author: docs9
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from mt5_api import Mt5Api
from common import TimeFrame
from datetime import datetime, timedelta
from dateutil import tz

JST = tz.gettz('Asia/Tokyo')
UTC = tz.gettz('utc') 

def download(symbols, save_holder):
    api = Mt5Api()
    api.connect()
    for symbol in symbols:
        for tf in [TimeFrame.M1, TimeFrame.M5, TimeFrame.M15, TimeFrame.M30, TimeFrame.H1, TimeFrame.H4, TimeFrame.D1]:
            for year in range(2018, 2025):
                for month in range(1, 13):
                    t0 = datetime(year, month, 1, 7)
                    t0 = t0.replace(tzinfo=JST)
                    t1 = t0 + relativedelta(months=1) - timedelta(seconds=1)
                    if tf == 'TICK':
                        rates = api.get_ticks(t0, t1)
                    else:
                        rates = api.get_rates_jst(symbol, tf, t0, t1)
                    path = os.path.join(save_holder, symbol, tf)
                    os.makedirs(path, exist_ok=True)
                    path = os.path.join(path, symbol + '_' + tf + '_' + str(year) + '_' + str(month).zfill(2) + '.csv')
                    df = pd.DataFrame(rates)
                    if len(df) > 10:
                        df.to_csv(path, index=False)
                    print(symbol, tf, year, '-', month, 'size: ', len(df))
    
    pass

def dl1():
    symbols = ['NIKKEI', 'DOW', 'NSDQ', 'SP', 'HK50', 'DAX', 'FTSE', 'XAUUSD']
    symbols += ['CL', 'USDJPY', 'GBPJPY']
    symbols += ['HK50', 'NGAS', 'EURJPY', 'AUDJPY', 'EURUSD']
    download(symbols, '../MarketData/Axiory/')
    
def dl2():
    symbols = ['SP', 'HK50', 'DAX', 'FTSE',  'XAGUSD', 'EURJPY', 'AUDJPY']
    symbols = ['NIKKEI', 'USDJPY']
    download(symbols, '../MarketData/Axiory/')
    
    
if __name__ == '__main__':
    dl1()

