
# Using a partial dataset from owid, create a dataframe with the necessary columns for the machine learning algorithm
# Then clean them up by prefilling NaN and None fields; changing the Date column to Date/Time format
# The output is written to a file in the data directory (data/input)


import numpy as np
import pandas as pd
import datetime
data_dir = "..\\sourcedata\\"

df = pd.read_csv(data_dir + 'owid-covid-data-project.csv')

df.head()

print((df['date'][0]))

print(type(df['date'][0]))

len(df)

# Show all ISO_CODEs
codes = df['iso_code'].unique()
codes

print('Number of ISO Codes:',len(codes))

# create a list of column names, then strip extra spaces and convert to upper case
cols = list(df.columns)
cols = [x.upper().strip() for x in cols]
df.columns = cols
df.head(0)

cols

type(cols)

# Convert date column to date/time type
df['DATE'] = pd.to_datetime(df['DATE'])

print(type(df['DATE'][0]))

df = df.set_index('ISO_CODE')
df.head()

for c in cols:
    print(c)

df[250:260]

df.loc['USA']

print(type(codes[0]))

# Fill in missing values using ffill; leading NaN values will NOT be replaced

#for cd in codes:
#    df.loc[cd] = df.loc[cd].fillna(method='ffill')

for alpha in range(len(codes) - 2):
    print('Processing ', codes[alpha])
    df.loc[codes[alpha]] = df.loc[codes[alpha]].fillna(method='ffill')

# Write df to a csv file
df.to_csv(data_dir+'testout.csv',index=False)



