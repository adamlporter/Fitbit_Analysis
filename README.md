# Fitbit_Analysis
Collection of Utilities to Process Fitbit data

There are multiple examples of using the Fitbit API to get data from Fitbit.
I have found it easier to use Fitbit's data export (https://www.fitbit.com/settings/data/export) and getting all the data for my account. These programs assume you have downloaded the zip file with all your data and put it into a working directory.

Four programs to process most FB data. Set the working directory and run the program. It will read through the FB data, clean it up, and create CSV files. See the DataFile_summary.txt file for discussion of how FB stores data about you.

The one set of data files I still need to work on is the exercise* files.

SimpleFilesToCSV.py
    altitude
    calories
    distance
    steps
    sedentary_minutes
    lightly_active_minutes
    moderately_active_minutes
    very_active_minutes

SleepDataToCSV.py
    sleep

HRLogToCSV.py
    hear_rate

HRZ_ToCSV.py
    time_in_heart_rate_zones
