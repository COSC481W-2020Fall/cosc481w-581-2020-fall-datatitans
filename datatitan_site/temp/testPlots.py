#!/usr/bin/env python
# coding: utf-8

# In[86]:
import inline as inline
import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
#%matplotlib inline

SMALL_SIZE = 8
MEDIUM_SIZE = 15
BIGGER_SIZE = 20

plt.rc('font', size=SMALL_SIZE)         # default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)    # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)   # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)   # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)   # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)   # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE) # fontsize of the figure title

df = pd.read_csv('owid-covid-data.csv') # import csv file to dataframe
df.head()

# In[87]:

#df.describe()                          # list out data frame
plt.figure(figsize=(50,20))             # set size of the graph
sns.set(font_scale=5)                   # set scale of graph fonts
sns.lineplot(data=df['total_deaths'])   # set line plot from data
#plt.ylim(0,250)                        # function to adjust the y limit
#plt.xlim(0,250)                        # function to adjust the x limit
plt.xticks(rotation=-45)                # add an angle to x labels

# In[4]:

dims = (100, 25)                        # dimension variable for plot area
fig, ax = plt.subplots(figsize=dims)    # set plot area size

g = sns.lineplot(x=df["date"], y=df["total_deaths"]) # line plot for full data
for ind, label in enumerate(g.get_xticklabels()):    # loop so not every xtick is show,
    if ind % 10 == 0:                                # making chart more readable
        label.set_visible(True)
    else:
        label.set_visible(False)

# In[88]:

us_data = df.query('location == "United States"') # Filter data by United States
fig, ax = plt.subplots(figsize=dims)              # set plot area size
sns.set(font_scale=4)                             # change to font scale

graph = sns.lineplot(x = us_data["date"], y = us_data["total_deaths"]) # line plot of only US data

for ind, label in enumerate(graph.get_xticklabels()): # loop so not every xtick is show,
    if ind % 10 == 0:                                 # making chart more readable
        label.set_visible(True)
    else:
        label.set_visible(False)

plt.show()                              # show plots


# In[8]:


df.describe()                           # list data


# In[91]:

dims = (50, 100)                        # set new dimension variable for plot area
fig, ax = plt.subplots(figsize=dims)    # set plot area size
sns.set(font_scale=2)                   # scale down font size
sns.barplot(x = df["total_deaths"], y = df["location"], ax=ax) # big bar graph of full original data frame

# In[92]:

# use the below line in CMD prompt to convert .ipynb to .py
#!jupyter nbconvert --to script covid.ipynb


