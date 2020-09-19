import os # to work with file system eg, relative and absolute paths
import matplotlib
import pandas as pd # Because pandas are cute and cuddly
import seaborn as sns # For plotting
import matplotlib.pyplot as plt # For showing plots

# Set paths for data and assign data file to appropriate path
path = os.getcwd()
parent = os.path.dirname(path)
DataDir = parent + "\sourcedata\\"
file = DataDir + 'owid-covid-data.csv'

df = pd.read_csv(file) # import csv file to dataframe
#print(df.head())

# function to take in 3-digit country code and chart type and return jpeg of that chart
def saveChart(country="USA", chartType="total_deaths"):
    #print(country, chartType)
    countryData = df.query('iso_code == @country')
    print(countryData.head())

saveChart("MEX", "total_cases")