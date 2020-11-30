# Using a partial dataset from owid, create a dataframe with the necessary columns for the machine learning algorithm
# Then clean them up by prefilling NaN and None fields; changing the Date column to Date/Time format
# The output is written to a file in the data directory (data/input)

import numpy as np
import pandas as pd
import datetime
from pathlib import Path

data_dir = Path(__file__).parent.parent / "input"

df = pd.read_csv(data_dir / "testdata.csv")
print(df.head())
print((df["date"][0]))
print(type(df["date"][0]))

len(df)

# Show all ISO_CODEs
codes = df["iso_code"].unique()
codes

# create a list of column names, then strip extra spaces and convert to upper case
cols = list(df.columns)
cols = [x.upper().strip() for x in cols]
df.columns = cols
df.head(0)

print(cols)
# print(type(cols))

# Convert date column to date/time type
df["DATE"] = pd.to_datetime(df["DATE"])

print(type(df["DATE"][0]))

df = df.set_index("ISO_CODE")
df.head()

for c in cols:
    print(c)

df[250:260]

c = "USA"
df.loc[c]

# Fill in missing values using ffill; leading NaN values will NOT be replaced

for c in codes:
    df.loc[c] = df.loc[c].fillna(method="ffill")

df[250:260]

# Write df to a csv file
df.to_csv(data_dir + "testout.csv", index=False)
