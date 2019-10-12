# Fitbit_Analysis
Collection of Utilities to Process Fitbit data

There are multiple examples of using the Fitbit API to get data from Fitbit.
I have found it easier to use Fitbit's data export (https://www.fitbit.com/settings/data/export) and getting all the data for my account. These programs assume you have downloaded the zip file with all your data and put it into a working directory.

I'm using Pandas, so the discussion below is done in terms of dataframes.

Sleep data is saved in month-long files. For each day, there is a row of summary data. In each row, there are two cells that have log data, that records the pattern of sleep from the time the user goes to bed until they get up. 

<b>ProcessSleepDataToCSV</b><P>
This program reads through the FB data directory and processes all the files named sleep-YYYY-MM-DD.json. It outputs two CSV files: <p>
sleepLog.csv -- the event-by-event sleep records<br>
sleepSummary.csv -- the daily summary of sleep information<p>
