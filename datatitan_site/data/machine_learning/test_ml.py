# NOTE: A coursera tutorial was used as the template for this code:
# https://www.coursera.org/learn/compare-time-series-predictions-of-covid19-deaths/home/welcome
#
# Until requirements.txt is updated, run from the command line:
# pipenv install statsmodels

# A script to test the SARIMAX ML algorithm on time series covid data
# The test data and trial data are both created from US Deaths, with a cutoff date the dividing point


import pandas as pd
import numpy as np
import datetime
import requests
import warnings

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima_model import ARIMA

warnings.filterwarnings("ignore")

# data is stored in the same directory
dataUSA = pd.read_csv("US-MainData.csv")

# dataUSA.head()

print(dataUSA.loc[:4, ["date", "new_deaths"]])

# Create an empty dataframe
deathsUSA = pd.DataFrame(columns=["Date", "New Deaths"])

# print(dataUSA.loc[58:80,['date','new_deaths']])

# rows contain zero deaths until approx. row 60
dates = dataUSA.loc[60:, "date"]
# print(dates.head())

# Convert to data format
dates = list(pd.to_datetime(dates))

# print(dates[:3])

deaths = dataUSA.loc[60:, "new_deaths"]
# print(deaths.head())

# Populate DataFrame
deathsUSA["New Deaths"] = deaths
deathsUSA["Date"] = dates

# Convert first column to the index
deathsUSA = deathsUSA.set_index("Date")

print(deathsUSA.tail())

plt.figure(figsize=(10, 10))
plt.plot(deathsUSA)
plt.savefig("Cummulative daily deaths", bbox_inches="tight", transparent=False)

# Set cutoff date at midway point of the date
cutoff_date = "2020-07-08"

# Although train and test can be different lengths, subsequent calcs may need same length
train = deathsUSA.loc[deathsUSA.index <= pd.to_datetime(cutoff_date)]
# Remove the = from <= above if lengths of train, test don't have to be equal
test = deathsUSA.loc[deathsUSA.index >= pd.to_datetime(cutoff_date)]
print(len(train), len(test))

model = SARIMAX(train, order=(2, 1, 3))  # Arrived at these 3 params by trial and error

results = model.fit(disp=True)

sarimax_prediction = results.predict(start=cutoff_date, end="2020-11-15", dynamic=False)
# print(len(sarimax_prediction))

plt.figure(figsize=(10, 5))
(l1,) = plt.plot(deathsUSA, label="Observation")
(l2,) = plt.plot(sarimax_prediction, label="Prediction")
plt.legend(handles=[l1, l2])
plt.savefig("SARIMAX prediction", bbox_inches="tight", transparent=False)
