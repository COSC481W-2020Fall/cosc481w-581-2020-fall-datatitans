# Code to read from a json file in the home directory and create a basic seaborn chart

import json
f = open('dataNA.json', 'r')
dictNA = json.load(f)

#print(dictNA['USA']['data'])



import pandas as pd # Because pandas are cute and cuddly
import seaborn as sns # For plotting
import matplotlib.pyplot as plt # For showing plots
import mpld3 #for generating html
cN = ["USA","CAN","MEX"]
for Q in cN:
    data = dictNA[Q]['data']
    df = pd.DataFrame(data)
    a = sns.lineplot(data=df, x = "date", y ="total_deaths")
    plt.title("total deaths in "+Q)
    plt.xlabel('Dates')
    plt.ylabel('Total Deaths')
    fig1 = plt.gcf()
    plt.show()
    plt.draw()
    fig1.savefig(Q+'1.jpeg', dpi=100)

# This next line doesn't work. We have to cast the "date" field as date and figure out how to
# show the dates on the x-axis
#sns.lineplot(x = df["date"], y = df["total_deaths"])
