import csv
from pathlib import Path
import numpy as np
import pandas as pd
import sqlite3


input_file_path = Path("owid-covid-data.csv")

with sqlite3.connect(":memory:") as conn:
    # conn.execute('''CREATE TABLE covid_data
    # (iso_code text not null , continent text, location text, date date,
    # new_cases integer default 0, new_deaths integer default 0, new_tests integer default 0)''')
    read_covid_data_raw = pd.read_csv(input_file_path)
    read_covid_data_raw.to_sql("COVID_DATA_RAW", conn, if_exists='replace', index=False)

