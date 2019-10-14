#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 08:49:10 2019

@author: adam
"""

import glob
import json
import pandas as pd
from pandas.io.json import json_normalize
import time

def dailySleepLog(idx,data_row):
    # input: index(ignored), data_row (1 day of data)
    # output: dataframe with 1 day's worth of sleep log data
    #
    # this fn takes the values from the 'levels.data' cell of the data row
    # and turns them into a df. 
    # Data cleaning - dateTime field into the proper format
    # convert all data in minutes (FB has milliseconds, seconds, minutes)
    # Add field for sleep offset (that is, how long from start of sleep various
    # actions take palce (this allows analysis of how long in a sleep session things happen)
    # add numerical value for sleep level
    
    from pandas.io.json import json_normalize

    log_temp = data_row['levels.data']
    log_temp_df = json_normalize(log_temp)
    log_temp_df['dateTime'] = pd.to_datetime(log_temp_df['dateTime'])
    log_temp_df['minutes'] = log_temp_df['seconds'].apply(lambda x: x/60)
    begTime = log_temp_df.loc[0]['dateTime']
    log_temp_df['deltaT'] = log_temp_df['dateTime'] - begTime
    # get_seconds = lambda offset: offset.seconds
    log_temp_df['deltaMin'] = log_temp_df['deltaT'].apply(lambda x: x.seconds/60)
    # create numeric value for sleep levels;this allows for combination of 
    # 'stages' and 'classic' data sets
    levelNums = {'awake':7,'restless':8,'asleep':9, # classic
                 'wake':1, 'light':2,'rem':3,'deep':4, # stages
                 'unknown':-1}
    log_temp_df['levelN'] = log_temp_df['level'].apply(lambda x: levelNums[x])   
    return(log_temp_df)
    
def cleanMontly(raw_df):
    # input: df of sleep data
    # output: cleaned df of sleep data
    #
    # cleaning: convert datatime strings to datetime
    # rename columns to use consistent mixed case format
    #
    # delte superfluvous columns (duration, infoCode, minutesToFallAsleep)
    #
    # "classic" is used for naps (<180 minutes?)
    # except for "restless" all its data is found in other fields, so 
    # delete those columns.
    #
    # delete the columns with daily sleep logs, since those have been
    # pulled out and saved separately
    #
    raw_df['dateOfSleep'] = pd.to_datetime(raw_df['dateOfSleep'])
    raw_df['startTime'] = pd.to_datetime(raw_df['startTime'])
    raw_df['endTime'] = pd.to_datetime(raw_df['endTime'])
    cols_rename = {'levels.summary.deep.minutes':'deepMinutes',
                   'levels.summary.deep.count':'deepCount',
                   'levels.summary.light.count':'lightCount',
                   'levels.summary.light.minutes':'lightMinutes',
                   'levels.summary.rem.count':'remCount',
                   'levels.summary.rem.minutes':'remMinutes',
                   'levels.summary.wake.count':'wakeCount', 
                   'levels.summary.wake.minutes':'wakeMinutes'
                   }
    cols_delete = ['duration',
                   'levels.summary.deep.thirtyDayAvgMinutes',
                   'levels.summary.light.thirtyDayAvgMinutes',
                   'levels.summary.rem.thirtyDayAvgMinutes',
                   'levels.summary.wake.thirtyDayAvgMinutes',
                   'minutesToFallAsleep',
                   'levels.data',
                   'levels.shortData'
                   ]
    add_cols   =  ['levels.summary.asleep.count',
                   'levels.summary.asleep.minutes', 
                   'levels.summary.awake.count',
                   'levels.summary.awake.minutes',
                   'levels.summary.restless.count',
                   'levels.summary.restless.minutes'
                   ]
                   
    raw_df.drop(cols_delete,axis = 1, inplace =True)
    if 'levels.summary.asleep.count' in raw_df.columns:
        raw_df.drop(add_cols,axis = 1, inplace =True)
        
    raw_df.rename(columns = cols_rename, inplace = True)
    return(raw_df)

workd = '/home/adam/Google Drive/Python/DataSets/Data_fitbit/'
sleepFiles = glob.glob(workd+'sleep*.json')

monthLogs=[]
sleepSummary = pd.DataFrame()
print('Processing ')
for fname in sleepFiles:
    print(fname)
    with open(fname, "r") as f:
        rawData=json.load(f)
        # create the main sleep df for the month
        sleepData = json_normalize(rawData)
        # the next line takes each row of the month and sends it to a fn that
        # returns a df of the raw sleep log data. Using a list comprehension it creates
        # a list of these dataframes
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
        dailyLogs = [dailySleepLog(index,row) for index, row in sleepData.iterrows()]
        
        # now clean up the data file
        sleepSummary = pd.concat([sleepSummary,cleanMontly(sleepData)])
    # list of dailyLog dfs is concated into the sleep log for the month
    monthLogs.extend(dailyLogs)
    
sleepLog = pd.concat(monthLogs)

date = time.strftime("%y%m%d"+"_"+"%H%M")

print('Files will be saved to directory with Fitbit datafiles with the following names:')
print('sleepLog_' + date + '.csv')
print('sleepSummary_' + date + '.csv')
  
sleepLog.to_csv(path_or_buf = workd + 'sleepLog_' + date + '.csv',index=False)
sleepSummary.to_csv(path_or_buf = workd + 'sleepSummary_' + date + '.csv',index=False)

