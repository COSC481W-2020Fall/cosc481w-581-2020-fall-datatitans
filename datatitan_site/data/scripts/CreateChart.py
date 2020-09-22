# import os  # to work with file system eg, relative and absolute paths
from pathlib import Path
import pandas as pd  # Because pandas are cute and cuddly
import seaborn as sns  # For plotting
import matplotlib.pyplot as plt  # For showing plots

SMALL_SIZE = 8
MEDIUM_SIZE = 15
BIGGER_SIZE = 20

plt.rc("font", size=SMALL_SIZE)  # default text sizes
plt.rc("axes", titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title

sns.set(font_scale=3)  # set scale of graph fonts
dims = (100, 25)  # dimension variable for plot area

fig, ax = plt.subplots(figsize=dims)  # set plot area size

# Set paths for data and assign data file to appropriate path
DataDir = Path(__file__).parent.parent / "input"
ImageDir = Path(__file__).parent.parent.parent / "images"

df = pd.read_csv(DataDir / "owid-covid-data.csv")  # import csv file to dataframe


# print(df.head())

# function to take in 3-digit country code and chart type and return jpeg of that chart


def saveChart(country="USA", chart_type="total_deaths"):
    # print(country, chartType)
    country_data = df.query("iso_code == @country")
    print(country_data.head())
    g = sns.lineplot(x=country_data["date"], y=country_data[chart_type])  # generate line plot
    for ind, label in enumerate(
        g.get_xticklabels()
    ):  # loop so not every xtick is show,
        if ind % 10 == 0:  # making chart more readable
            label.set_visible(True)
        else:
            label.set_visible(False)

    plt.title(country)
    plt.autoscale()  # adjust frame for labels
    plt.xticks(rotation=-45)  # add an angle to x labels
    plt.savefig(ImageDir / "plot.jpeg")


# saveChart("MEX", "total_cases")
