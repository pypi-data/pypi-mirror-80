#!/usr/bin/env python
#----------------------------------------------------------------------------
# pseanalytics.py
# 
# Module containing all common methods for pulling Stock data from
# https://www.investagrams.com/Stock
# 
# get_stock_data - generates dataframe for a give stock for a given duration
# 
# kentballon@gmail.com
# 
#----------------------------------------------------------------------------
# Imports
import os
import pandas as pd
import numpy as np
from datetime import datetime

#----------------------------------------------------------------------------
# Global Variables
# defining the api-endpoint  
api_endpoint = "https://www.investagrams.com/Stock/"
# filters for data from web scrape
filters = ['<td class="table-info">','<td>','</td>','<td class="table-danger">','<td class="table-success">','<td,class="table-warning">','<td class="table-warning">','\r',',']
# delimiter used for the datapoints
delimiter = "</td>" 
# columns used for dataframe 
df_columns = ['stock','date','close','change','pchange','open','low','high','volume','netforeign']
#----------------------------------------------------------------------------

def get_uniq_stock_keys(df):
  keys = df['stock'].unique()
  return keys

# Adjust the units present in some datapoints
def post_fix_correction(string):
    retval = string

    correction = {"B":1000000000,"M":1000000,"K":1000,"%":1}

    for keys in correction:
        if keys in string:
            string = string.replace(keys,"")
            retval = float(string) * correction[keys] 

    return retval

# Compute the Exponential Moving Averages
def get_ema(df):
    # calculate EMA
    df['ema9'] = df.iloc[:,1].ewm(span=9,adjust=False).mean()
    df['ema12'] = df.iloc[:,1].ewm(span=12,adjust=False).mean()
    df['ema20'] = df.iloc[:,1].ewm(span=20,adjust=False).mean()
    df['ema26'] = df.iloc[:,1].ewm(span=26,adjust=False).mean()
    df['ema50'] = df.iloc[:,1].ewm(span=50,adjust=False).mean()
    df['ema52'] = df.iloc[:,1].ewm(span=52,adjust=False).mean()
    df['ema100'] = df.iloc[:,1].ewm(span=100,adjust=False).mean()
    return df

# Compute the MACD
def get_macd(df):
    # calculate MACD
    df['macd'] = df['ema12'] - df['ema26']
    df['macds'] = df.iloc[:,15].ewm(span=9,adjust=False).mean()
    return df

# Compute the RSI
def get_rsi(data, time_window):
    # reference: https://tcoil.info/compute-rsi-for-stocks-with-python-relative-strength-index/
    diff = data.diff(1).dropna()        # diff in one field(one day)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff
    
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]
    
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]
    
    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi

def get_candlestick(df):
    # calculate candlestick patterns
    # add open to head column
    df['openh']= df['high'] - df['open']
    # add close to head column
    df['closeh']= df['high'] - df['close']
    # add open to tail column
    df['opent']= df['open'] - df['low']
    # add close to tail column
    df['closet']= df['close'] - df['low']
    # add body column
    df['body'] = abs(df['close'] - df['open'])
    return df

def get_alma(df):
    # reference: https://github.com/darwinsys/Trading_Strategies/blob/master/ML/Features.py
    # window
    length = 20
    # just some number (6.0 is useful)
    sigma = 6
    # sensisitivity (close to 1) or smoothness (close to 0)
    offset = .85

    asize = length - 1
    m = np.floor(offset * asize)
    s = length  / sigma
    dss = 2 * s * s

    alma = np.zeros(df.shape)
    wtd_sum = np.zeros(df.shape)

    for l in range(len(df)):
        if l >= asize:
            for i in range(length):
                im = i - m
                wtd = np.exp( -(im * im) / dss)
                alma[l] += df[l - length + i] * wtd
                wtd_sum[l] += wtd
            alma[l] = alma[l] / wtd_sum[l]
    return alma

# Main function to pull stock data
def get_stock_data(stock,start_date="2020-01-02",end_date="2020-01-02"):

    # get all stock data available
    command = "curl -s " + api_endpoint + stock + " | grep table-info | awk -F 'table-info\">' '{print $2}'"
    stream = os.popen(command)
    output = stream.read()

    # remove filter words
    for f in filters:
        if (f == delimiter ):
          output = output.replace(f,"|")
        else:
          output = output.replace(f,"")

    outputarr = output.split('\n')

    # prepare dataframe input
    data = []
    for entry in outputarr:
        if not entry == "" :
            list_entry = entry.split("|")[:-1]
            dt_string = list_entry[0]
            # format date
            list_entry[0] = datetime.strptime(dt_string, "%b %d %Y")
            # format pchange 
            list_entry[3] = post_fix_correction(list_entry[3])
            # format volume
            list_entry[7] = post_fix_correction(list_entry[7])
            # format netforeign
            list_entry[8] = post_fix_correction(list_entry[8])
            # add stock code
            list_entry.insert(0,stock)
            data.insert(0,list_entry)
    
    # create dataframe
    df = pd.DataFrame(data, columns=df_columns)

    # format all columns as float except for date
    for col in df.columns:
        if not (col in ("date","stock")):
            df[col] = df[col].astype(float)

    # set date as search index
    df = df.set_index(['date'])

    # calculate EMA
    df = get_ema(df)
    # calculate MACD
    df = get_macd(df)
    # calculate RSI
    df['rsi'] = get_rsi(df['close'],14)
    # calculate ALMA
    df['alma'] = get_alma(df['close'])
    # calculate Candlestick patterns
    df = get_candlestick(df) 
 
    # limit dataframe to date range
    df = df.loc[start_date:end_date]
    # reset the index
    df = df.reset_index()
    # sort by date
    df.sort_values(by=['date'], inplace=True, ascending=True)

    return df 
