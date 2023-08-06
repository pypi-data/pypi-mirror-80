#!/usr/bin/env python
# ------------------------------------------------------------------------------------------------------
# strategies.py
#
# Collection of methods implementing trading strategies based on specified 
# criteria and identifies potential trades
# 
# kentballon@gmail.com
#
# ------------------------------------------------------------------------------------------------------
import pandas as pd
import sys
import pseanalytics as pseapi
from datetime import date, datetime, timedelta

class whitesoldier:

    def __init__(self,csv_file_name,report_date,trendfac = 3,resfac = 1,supfac = 1,pc_fac = 0,volfac1 = 1000000,volfac2 = 500000,volfac3 = 10000000,netffac = 0,pc_crit = 2,volfac_crit = 16,res_crit = 0,sup_crit = 0):
        # list of stock code to evaluate
        self.csv_file_name = csv_file_name
        # date to evaluate
        self.report_date = report_date
        # number of days to sample for the observation 
        self.trendfac = trendfac
        # adjust head factor relative to body 
        self.resfac = resfac
        # adjust tail factor relative to body 
        self.supfac = supfac
        # percent change to consider 
        self.pc_fac = pc_fac
        # trade volume targets
        self.volfac1 = volfac1 
        self.volfac2 = volfac2
        self.volfac3 = volfac3
        # net foreign factor
        self.netffac = netffac
        # result criteria
        self.pc_crit = pc_crit 
        self.volfac_crit = (self.volfac1 + self.volfac2 + self.volfac3)/(self.volfac1)
        self.res_crit = res_crit 
        self.sup_crit = sup_crit 
    
    def get_whitesoldier_score(self,df, keys,trendfac,resfac,supfac,pc_fac,volfac1,volfac2,volfac3,netffac,pc_crit,volfac_crit,res_crit,sup_crit):
      # create dataframe for overall tally
      df_score = pd.DataFrame(columns=['stock', 'volume_score', 'pchange_score','resistance_score','support_score','net_foreign_score'])
      for key in keys:
        volume_score = 0
        pchange_score = 0
        support_score = 0
        resistance_score = 0
        net_foreign_score = 0
    
        df_subset = df[df.stock == key]
        df_subset = df_subset.tail(int(trendfac))
        for ind in df_subset.index:
    
          # compute volume criteria
          if (df_subset['volume'][ind] >= volfac3):
            volume_score = volume_score + 3
          elif (df_subset['volume'][ind] >= volfac2):
            volume_score = volume_score + 2
          elif (df_subset['volume'][ind] >= volfac1):
            volume_score = volume_score + 1
          else:
            volume_score = volume_score - 2
    
          # compute percent change criteria
          if (df_subset['pchange'][ind] > pc_fac):
            pchange_score = pchange_score + 1
          #else:
          #  pchange_score = pchange_score - 1
    
          # compute resistance criteria
          if (df_subset['pchange'][ind] > 0):
            if (df_subset['closeh'][ind] >= (resfac * df_subset['body'][ind])):
              resistance_score = resistance_score + 1
            #else:
            #  resistance_score = resistance_score - 1
          else:
            if (df_subset['openh'][ind] >= (resfac * df_subset['body'][ind])):
              resistance_score = resistance_score + 1
            #else:
            #  resistance_score = resistance_score - 1
    
          # compute support criteria
          if (df_subset['pchange'][ind] > 0):
            if (df_subset['opent'][ind] >= (supfac * df_subset['body'][ind])):
              support_score = support_score + 1
            #else:
            #  support_score = support_score - 1
          else:
            if (df_subset['closet'][ind] >= (supfac * df_subset['body'][ind])):
              support_score = support_score + 1
            #else:
            #  support_score = support_score - 1
    
          # compute percent change criteria
          if (df_subset['netforeign'][ind] > netffac):
            net_foreign_score = net_foreign_score + 1
          #else:
          #  net_foreign_score = net_foreign_score - 1
     
        # check overall condition
        if (volume_score >= volfac_crit 
            and pchange_score >= pc_crit
            and resistance_score >= res_crit 
            and support_score >= sup_crit 
           ):
          df_score = df_score.append({'stock': key, 
                                      'volume_score': volume_score, 
                                      'pchange_score': pchange_score, 
                                      'resistance_score': resistance_score, 
                                      'support_score': support_score, 
                                      'net_foreign_score': net_foreign_score}, 
                                      ignore_index=True)
      return df_score
        
    def get_whitesoldier_stocks(self,df, keys,trendfac):
        retdf=pd.DataFrame()
        for key in keys:
            df_subset = df[df.stock == key]
            df_subset = df_subset.tail(int(trendfac))
            retdf = retdf.append(df_subset,ignore_index = True)
        return retdf
    
    def get_stock_data(self):
        df = pd.read_csv(self.csv_file_name)
        report_date = datetime.strptime(self.report_date, "%Y-%m-%d")
        report_date_n_days_ago = report_date - timedelta(days=self.trendfac)
        report_date = report_date.strftime("%Y-%m-%d")
        report_date_n_days_ago = report_date_n_days_ago.strftime("%Y-%m-%d")
    
        fulldata=pd.DataFrame()
        for stock in df['stock']:
            data = pseapi.get_stock_data(stock,report_date_n_days_ago,report_date)
            data = data.round(2)
            fulldata = fulldata.append(data,ignore_index = True)
    
        keys = pseapi.get_uniq_stock_keys(fulldata)
        filtered_df_score = self.get_whitesoldier_score(fulldata, keys,self.trendfac,self.resfac,self.supfac,self.pc_fac,self.volfac1,self.volfac2,self.volfac3,self.netffac,self.pc_crit,self.volfac_crit,self.res_crit,self.sup_crit)
        filtered_keys = pseapi.get_uniq_stock_keys(filtered_df_score)
        filtered_df = self.get_whitesoldier_stocks(fulldata,filtered_keys,self.trendfac)
    
        return filtered_df, filtered_df_score

class macd_crossing:
    def __init__(self,csv_file_name,report_date,trendfac = 0):
        # list of stock code to evaluate
        self.csv_file_name = csv_file_name
        # date to evaluate
        self.report_date = report_date
        # number of days to sample for the observation 
        self.trendfac = trendfac

    def get_stock_data(self):
        df = pd.read_csv(self.csv_file_name)
        report_date = datetime.strptime(self.report_date, "%Y-%m-%d")
        report_date_n_days_ago = report_date - timedelta(days=self.trendfac)
        report_date = report_date.strftime("%Y-%m-%d")
        report_date_n_days_ago = report_date_n_days_ago.strftime("%Y-%m-%d")
        fulldata=pd.DataFrame()
        for stock in df['stock']:
            data = pseapi.get_stock_data(stock,report_date_n_days_ago,self.report_date)
            data = data.round(2)
            filtered_df = data.loc[abs(data['macd'] - data['macds']) == 0]
            fulldata = fulldata.append(filtered_df,ignore_index = True)

        return fulldata

class rsi_oversold:
    def __init__(self,csv_file_name,report_date,trendfac = 0, limit = 30):
        # list of stock code to evaluate
        self.csv_file_name = csv_file_name
        # date to evaluate
        self.report_date = report_date
        # number of days to sample for the observation 
        self.trendfac = trendfac
        # oversold threshold
        self.limit = limit 

    def get_stock_data(self):
        df = pd.read_csv(self.csv_file_name)
        report_date = datetime.strptime(self.report_date, "%Y-%m-%d")
        report_date_n_days_ago = report_date - timedelta(days=self.trendfac)
        report_date = report_date.strftime("%Y-%m-%d")
        report_date_n_days_ago = report_date_n_days_ago.strftime("%Y-%m-%d")
        fulldata=pd.DataFrame()
        for stock in df['stock']:
            data = pseapi.get_stock_data(stock,report_date_n_days_ago,self.report_date)
            data = data.round(2)
            filtered_df = data.loc[data['rsi'] <= self.limit]
            fulldata = fulldata.append(filtered_df,ignore_index = True)

        return fulldata

class rsi_overbought:
    def __init__(self,csv_file_name,report_date,trendfac = 0, limit = 70):
        # list of stock code to evaluate
        self.csv_file_name = csv_file_name
        # date to evaluate
        self.report_date = report_date
        # number of days to sample for the observation 
        self.trendfac = trendfac
        # overbought threshold
        self.limit = limit 

    def get_stock_data(self):
        df = pd.read_csv(self.csv_file_name)
        report_date = datetime.strptime(self.report_date, "%Y-%m-%d")
        report_date_n_days_ago = report_date - timedelta(days=self.trendfac)
        report_date = report_date.strftime("%Y-%m-%d")
        report_date_n_days_ago = report_date_n_days_ago.strftime("%Y-%m-%d")
        fulldata=pd.DataFrame()
        for stock in df['stock']:
            data = pseapi.get_stock_data(stock,report_date_n_days_ago,self.report_date)
            data = data.round(2)
            filtered_df = data.loc[data['rsi'] >= self.limit]
            fulldata = fulldata.append(filtered_df,ignore_index = True)

        return fulldata

class ema52low:
    def __init__(self,csv_file_name,report_date,trendfac = 0):
        # list of stock code to evaluate
        self.csv_file_name = csv_file_name
        # date to evaluate
        self.report_date = report_date
        # number of days to sample for the observation 
        self.trendfac = trendfac

    def get_stock_data(self):
        df = pd.read_csv(self.csv_file_name)
        report_date = datetime.strptime(self.report_date, "%Y-%m-%d")
        report_date_n_days_ago = report_date - timedelta(days=self.trendfac)
        report_date = report_date.strftime("%Y-%m-%d")
        report_date_n_days_ago = report_date_n_days_ago.strftime("%Y-%m-%d")
        fulldata=pd.DataFrame()
        for stock in df['stock']:
            data = pseapi.get_stock_data(stock,report_date_n_days_ago,self.report_date)
            data = data.round(2)
            filtered_df = data.loc[data['close'] <= data['ema52']]
            fulldata = fulldata.append(filtered_df,ignore_index = True)

        return fulldata

class marketsummary:
    def __init__(self,csv_file_name,report_date,trendfac = 0):
        # list of stock code to evaluate
        self.csv_file_name = csv_file_name
        # date to evaluate
        self.report_date = report_date
        # number of days to sample for the observation 
        self.trendfac = trendfac

    def get_stock_data(self):
        df = pd.read_csv(self.csv_file_name)
        report_date = datetime.strptime(self.report_date, "%Y-%m-%d")
        report_date_n_days_ago = report_date - timedelta(days=self.trendfac)
        report_date = report_date.strftime("%Y-%m-%d")
        report_date_n_days_ago = report_date_n_days_ago.strftime("%Y-%m-%d")
        fulldata=pd.DataFrame()
        for stock in df['stock']:
            data = pseapi.get_stock_data(stock,report_date_n_days_ago,self.report_date)
            data = data.round(2)
            fulldata = fulldata.append(data,ignore_index = True)

        return fulldata

class marketvolume:
    def __init__(self,csv_file_name,report_date,trendfac = 0):
        # list of stock code to evaluate
        self.csv_file_name = csv_file_name
        # date to evaluate
        self.report_date = report_date
        # number of days to sample for the observation 
        self.trendfac = trendfac

    def get_stock_data(self):
        df = pd.read_csv(self.csv_file_name)
        report_date = datetime.strptime(self.report_date, "%Y-%m-%d")
        report_date_n_days_ago = report_date - timedelta(days=self.trendfac)
        report_date = report_date.strftime("%Y-%m-%d")
        report_date_n_days_ago = report_date_n_days_ago.strftime("%Y-%m-%d")
        fulldata=pd.DataFrame()
        for stock in df['stock']:
            data = pseapi.get_stock_data(stock,report_date_n_days_ago,self.report_date)
            data = data.round(2)
            fulldata = fulldata.append(data,ignore_index = True)

        fulldata.sort_values(by=['volume'], inplace=True, ascending=True)
        return fulldata

class alma:
    def __init__(self,csv_file_name,report_date,trendfac = 0):
        # list of stock code to evaluate
        self.csv_file_name = csv_file_name
        # date to evaluate
        self.report_date = report_date
        # number of days to sample for the observation 
        self.trendfac = trendfac

    def get_stock_data(self):
        df = pd.read_csv(self.csv_file_name)
        report_date = datetime.strptime(self.report_date, "%Y-%m-%d")
        report_date_n_days_ago = report_date - timedelta(days=self.trendfac)
        report_date = report_date.strftime("%Y-%m-%d")
        report_date_n_days_ago = report_date_n_days_ago.strftime("%Y-%m-%d")
        fulldata=pd.DataFrame()
        for stock in df['stock']:
            data = pseapi.get_stock_data(stock,report_date_n_days_ago,self.report_date)
            data = data.round(2)
            filtered_df = data.loc[data['close'] >= data['alma']]
            fulldata = fulldata.append(filtered_df,ignore_index = True)

        return fulldata
