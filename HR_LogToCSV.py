#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 11:40:19 2019

@author: adam
"""

import json
import pandas as pd
import glob
import time

def processFile(fName):
    # open the file, import the json data, and convert data from strings to 
    # datetime and numeric values
    
    from pandas.io.json import json_normalize
    with open(fname, "r") as f:
        rawData = json_normalize(json.load(f))
        rawData['dateTime'] = pd.to_datetime(rawData['dateTime'])
        
        cols_rename = {'value.bpm' : 'bpm',
                       'value.confidence' : 'confidence'
                       }
        rawData.rename(columns = cols_rename, inplace = True)                         
        
    return(rawData)
    
def fixDateTime(workdf):
    # from pytz import all_timezones
    # all_timezones can be searched or printed to find out the correct name/format
    # for differnt local TZs
    #
    # some data stores DT in UTC. This procedure will convert 'dateTime' from 
    # UTC into the local TZ and return the dataframe
    import pytz # need to convert UTC data to local TZ
    from pytz import timezone

    local = pytz.timezone('US/Central')
    workdf['dateTime'] = workdf['dateTime'].apply(lambda x: pytz.UTC.localize(x))
    workdf['localDT'] = workdf['dateTime'].apply(lambda x: x.astimezone(local))
    workdf['dateTime'] = workdf['localDT']
    return(workdf)

workd = '/home/adam/Google Drive/Python/DataSets/Data_fitbit/'

dataTypes = ['heart_rate']
# the following data types are recorded in UTC

print('Files will be saved to directory with Fitbit datafiles with the following name:')
print('Processing:')

for dt in dataTypes:
    dataFiles = glob.glob(workd+dt+'*.json')
    toSaveData = pd.DataFrame()
    for fname in dataFiles:
        print(fname)
        toSaveData = pd.concat([toSaveData,processFile(fname)])

    toSaveData = fixDateTime(toSaveData)

date = time.strftime("%y%m%d"+"_"+"%H%M")
print('Saving -> '+dt+'Data_' + date + '.csv')
toSaveData.to_csv(path_or_buf = workd + dt +'Data_' + date + '.csv',index=False)
    
HRlog = toSaveData

