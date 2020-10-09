# Testing ground to practice new data visualization tools like scatter plots, box plots, etc
# For now, it just prints summary info about the data

# import os # to work with file system eg, relative and absolute paths
import matplotlib
import pandas as pd # Because pandas are cute and cuddly
import seaborn as sns # For plotting
import matplotlib.pyplot as plt # For showing plots

# Set paths for data, images
# path = os.getcwd()
#parent = os.path.dirname(path)
# DataDir = parent + "\sourcedata\\"

file = '..\input\owid-covid-data.csv'

df = pd.read_csv(file) # import csv file to dataframe
#print(df.head())

print(df.head())

print(df.describe())