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
        cols_rename = {'value.valuesInZones.BELOW_DEFAULT_ZONE_1' : 'below1',
                       'value.valuesInZones.IN_DEFAULT_ZONE_1' : 'zone1',
                       'value.valuesInZones.IN_DEFAULT_ZONE_2' : 'zone2',
                       'value.valuesInZones.IN_DEFAULT_ZONE_3' : 'zone3'
                       }
        rawData.rename(columns = cols_rename, inplace = True)                         
    return(rawData)

workd = '/home/adam/Google Drive/Python/DataSets/Data_fitbit/'

dataTypes = ['time_in_heart_rate_zones']
# the following data types are recorded in UTC

print('Files will be saved to directory with Fitbit datafiles with the following name:')
print('Processing:')

for dt in dataTypes:
    dataFiles = glob.glob(workd+dt+'*.json')
    toSaveData = pd.DataFrame()
    for fname in dataFiles:
        print(fname)
        toSaveData = pd.concat([toSaveData,processFile(fname)])

HRZdf = toSaveData

date = time.strftime("%y%m%d"+"_"+"%H%M")
print('Saving -> '+dt+'Data_' + date + '.csv')
toSaveData.to_csv(path_or_buf = workd + dt +'Data_' + date + '.csv',index=False)
