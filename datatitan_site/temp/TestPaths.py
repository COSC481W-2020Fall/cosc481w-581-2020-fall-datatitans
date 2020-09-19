# Showing how to use path references in python to navigate to data directory
import os  # to work with file system eg, relative and absolute paths
import pandas as pd  # Because pandas are cute and cuddly
import seaborn as sns  # For plotting
import matplotlib.pyplot as plt  # For showing plots

path = os.getcwd()
parent = os.path.dirname(path)

print("Current path:", path)
print("Parent directory:", parent)
DataDir = parent + "\\data\\sourcedata\\"
ImageDir = parent + "\\images\\"

print("Data directory:", DataDir)
f = DataDir + "owid-covid-data.csv"
print("File:", f)

df = pd.read_csv(f)  # import csv file to dataframe

# print(df.describe())
print(df.head())

sns.lineplot(data=df["total_deaths"])
plt.show()
outputFile = ImageDir + "total_deaths.jpeg"
# plt.savefig(outputFile)
