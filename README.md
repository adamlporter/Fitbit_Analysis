# Fitbit_Analysis
Collection of Utilities to Process Fitbit data

There are multiple examples of using the Fitbit API to get data from Fitbit.
I have found it easier to use Fitbit's data export (https://www.fitbit.com/settings/data/export) and getting all the data for my account. These programs assume you have downloaded the zip file with all your data and put it into a working directory.

Sleep data is saved in month files.
Each row of data has (a) summary information for one day and (b) two cells that log sleep events (level of sleep, time it started, etc.).

<b>SleepDataToCSV</b> reads through the FB data directory and processes all the files named sleep-YYYY-MM-DD.json. It outputs two CSV files, that could be analyzed in any program.<p>
sleepLog.csv -- the event-by-event sleep records<br>
sleepSummary.csv -- the daily summary of sleep information<p>

To come: examples of analysis of this data.
