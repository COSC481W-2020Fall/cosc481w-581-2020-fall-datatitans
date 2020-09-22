# Code to read from a json file in the home directory and create a basic seaborn chart

import json
import pandas as pd  # Because pandas are cute and cuddly
import seaborn as sns  # For plotting
import matplotlib.pyplot as plt  # For showing plots
import mpld3  # for generating html
from pathlib import Path


# print(dictNA['USA']['data'])


def gen_images():
    with Path(__file__).parent / "dataNA.json" as f:
        dictNA = json.load(f.open('r'))
    ImageDir = Path(__file__).parent.parent / "data" / "static"

    cN = ["USA", "CAN", "MEX"]
    for Q in cN:
        data = dictNA[Q]['data']
        df = pd.DataFrame(data)
        a = sns.lineplot(data=df, x = "date", y ="total_cases")
        plt.title("total cases in "+Q)
        plt.xlabel('Dates')
        plt.ylabel('Total Deaths')
        fig1 = plt.gcf()
        plt.draw()
        fileN = Q+'1.jpeg'
        fig1.savefig(ImageDir / fileN, dpi=100)
        plt.close(fig1)

    for W in cN:
        data = dictNA[W]['data']
        df = pd.DataFrame(data)
        a = sns.lineplot(data=df, x = "date", y ="total_deaths")
        plt.title("total deaths in "+W)
        plt.xlabel('Dates')
        plt.ylabel('Deaths')
        fig1 = plt.gcf()
        plt.draw()
        fileN = W+'2.jpeg'
        fig1.savefig(ImageDir / fileN, dpi=100)
        plt.close(fig1)

    # This next line doesn't work. We have to cast the "date" field as date and figure out how to
    # show the dates on the x-axis
    # sns.lineplot(x = df["date"], y = df["total_deaths"])
