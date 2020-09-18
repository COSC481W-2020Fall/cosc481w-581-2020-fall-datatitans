from pathlib import Path
import pandas as pd
import sqlite3
from datatitan_site.settings import DATABASES
from datetime import date


input_file_path = Path(f"{Path(__file__).parent}/input/owid-covid-data.csv")
# database_path = Path(f"{Path(__file__).parent}/database/test_database.db")

if (
        not input_file_path.exists()
        or date.fromtimestamp(input_file_path.stat().st_ctime) < date.today()
):
    print(f"File Exists: {input_file_path.exists()}")
    if input_file_path.exists():
        print(
            f"File created on:{date.fromtimestamp(input_file_path.stat().st_ctime).today()}\n"
            f"Current Date: {date.today()}"
        )


with sqlite3.connect(DATABASES["default"]["NAME"]) as conn:
    read_covid_data_raw = pd.read_csv(input_file_path)
    read_covid_data_raw.to_sql("COVID_DATA_RAW", conn, if_exists="replace", index=False)
    conn.executescript(
        """
        drop view if exists COVID_DATA_CLEAN;
        CREATE VIEW COVID_DATA_CLEAN as
        select iso_code,
               continent,
               location,
               date,
               coalesce(cast(new_cases as integer), 0) as new_cases,
               sum(new_cases) over (partition by iso_code rows between unbounded preceding and current row)
               as total_cases,
               coalesce(cast(new_deaths as integer), 0) as new_deaths,
               sum(new_deaths) over (partition by iso_code rows between unbounded preceding and current row)
               as total_deaths,
               coalesce(cast(new_tests as integer), 0) as new_tests,
               sum(new_tests) over (partition by iso_code rows between unbounded preceding and current row)
               as total_tests
        from COVID_DATA_RAW
        order by iso_code, date;
        """
    )
