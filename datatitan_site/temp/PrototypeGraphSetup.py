# Code to read from a json file in the home directory and create a basic seaborn chart

import json
import pandas as pd  # Because pandas are cute and cuddly
import seaborn as sns  # For plotting
import matplotlib.pyplot as plt  # For showing plots
import mpld3  # for generating html
from pathlib import Path


# print(dictNA['USA']['data'])

SMALL_SIZE = 5
SMALLER_SIZE = 3
MEDIUM_SIZE = 15
BIGGER_SIZE = 20

plt.rc("font", size=SMALL_SIZE)  # default text sizes
plt.rc("axes", titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=SMALLER_SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=BIGGER_SIZE)  # legend fontsize
plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title


def gen_images():
    with (Path(__file__).parent / "dataNA.json").open("r") as f:
        dictNA = json.load(f)
    ImageDir = Path(__file__).parent.parent / "data/static"

    cN = ["USA", "CAN", "MEX"]
    for Q in cN:
        data = dictNA[Q]["data"]
        df = pd.DataFrame(data)
        a = sns.lineplot(data=df, x="date", y="total_cases")
        for ind, label in enumerate(
            a.get_xticklabels()
        ):  # loop so not every xtick is show,
            if ind % 10 == 0:  # making chart more readable
                label.set_visible(True)
            else:
                label.set_visible(False)
        plt.title("total cases in " + Q)
        plt.xlabel("Dates")
        plt.ylabel("Total Cases")
        plt.xticks(rotation=-45)  # add an angle to x labels
        fig1 = plt.gcf()
        plt.draw()
        fig1.savefig(ImageDir / (Q + "1.jpeg"), dpi=400)
        plt.close(fig1)

    for W in cN:
        data = dictNA[W]["data"]
        df = pd.DataFrame(data)
        a = sns.lineplot(data=df, x="date", y="total_deaths")
        for ind, label in enumerate(
            a.get_xticklabels()
        ):  # loop so not every xtick is show,
            if ind % 10 == 0:  # making chart more readable
                label.set_visible(True)
            else:
                label.set_visible(False)
        plt.title("total deaths in " + W)
        plt.xlabel("Dates")
        plt.ylabel("Total Deaths")
        plt.xticks(rotation=-45)  # add an angle to x labels
        fig1 = plt.gcf()
        plt.draw()
        fig1.savefig(ImageDir / (W + "2.jpeg"), dpi=400)
        plt.close(fig1)

    # This next line doesn't work. We have to cast the "date" field as date and figure out how to
    # show the dates on the x-axis
    # sns.lineplot(x = df["date"], y = df["total_deaths"])
