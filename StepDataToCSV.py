#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 10:29:18 2019

@author: adam
"""

import json
from pandas.io.json import json_normalize
import pandas as pd
import pytz # need to convert UTC data to local TZ
from pytz import timezone
import glob
import time

local = pytz.timezone('US/Central')
# from pytz import all_timezones
# all_timezones can be searched or printed to find out the correct name/format
# for differnt locals
workd = '/home/adam/Google Drive/Python/DataSets/Data_fitbit/'

sleepFiles = glob.glob(workd+'step*.json')
stepData = pd.DataFrame()
print('Processing:')

for fname in sleepFiles:
    print(fname)
    with open(fname, "r") as f:
        rawSteps = json_normalize(json.load(f))
        
        # convert to datetime, mark as UTC, and add column for localized timestamp
        rawSteps['dateTime'] = pd.to_datetime(rawSteps['dateTime'])
        rawSteps['dateTime'] = rawSteps['dateTime'].apply(lambda x: pytz.UTC.localize(x))
        rawSteps['localDT'] = rawSteps['dateTime'].apply(lambda x: x.astimezone(local))
        rawSteps['value'] = pd.to_numeric(rawSteps['value'])
        
        stepData = pd.concat([stepData,rawSteps])

date = time.strftime("%y%m%d"+"_"+"%H%M")

print('Files will be saved to directory with Fitbit datafiles with the following name:')
print('stepData_' + date + '.csv')
  
stepData.to_csv(path_or_buf = workd + 'stepData_' + date + '.csv',index=False)

'''

dailySummary = rawSteps.groupby(rawSteps['dateTime'].dt.dayofyear).sum()
hourlySummary

# add DOY to allow analysis (not needed?)
rawSteps['doy'] = rawSteps['dateTime'].dt.dayofyear

# visualizations
import seaborn as sns
sns.set(style='whitegrid')

ax = sns.barplot(y=rawSteps['value'],x=rawSteps['dateTime'].dt.dayofyear)
ax = sns.barplot(y=rawSteps['value'],x=rawSteps['dateTime'].dt.hour)

ax = sns.barplot(y=rawSteps['value'],
                  x=rawSteps['localDT'].dt.dayofyear).
                  set(xticks=())
'''