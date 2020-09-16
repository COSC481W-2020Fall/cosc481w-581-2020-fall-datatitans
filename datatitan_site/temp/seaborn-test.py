# Code to read from a json file in the home directory and create a basic seaborn chart

import json
f = open('dataNA.json', 'r')
dictNA = json.load(f)

print(dictNA['USA']['data'])

dataUSA = dictNA['USA']['data']

import pandas as pd # Because pandas are cute and cuddly
import seaborn as sns # For plotting
import matplotlib.pyplot as plt # For showing plots

df = pd.DataFrame(dataUSA)
print(df)

df.describe()

sns.lineplot(data=df['total_deaths'])

# This next line doesn't work. We have to cast the "date" field as date and figure out how to
# show the dates on the x-axis
sns.lineplot(x = df["date"], y = df["total_deaths"])
