# Showing how to use path references in python to navigate to data directory
# import os  # to work with file system eg, relative and absolute paths
from pathlib import Path
import pandas as pd  # Because pandas are cute and cuddly
import seaborn as sns  # For plotting
import matplotlib.pyplot as plt  # For showing plots

DataDir = Path(__file__).parent.parent / "data/input"
ImageDir = Path(__file__).parent.parent / "images"

print("Data directory:", DataDir)
with DataDir / "owid-covid-data.csv" as f:
    print("File:", f)

    df = pd.read_csv(f)  # import csv file to dataframe

# print(df.describe())
print(df.head())

sns.lineplot(data=df["total_deaths"])
plt.show()
outputFile = ImageDir / "total_deaths.jpeg"
# plt.savefig(outputFile)
