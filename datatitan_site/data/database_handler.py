from pathlib import Path
import pandas as pd
import sqlite3
from datatitan_site.settings import DATABASES
from datetime import date
from .models import CovidDataRaw


input_file_path = Path(f"{Path(__file__).parent}/input/owid-covid-data.csv")
# database_path = Path(f"{Path(__file__).parent}/database/test_database.db")


def input_missing_or_outdated():
    return (not input_file_path.exists()) or date.fromtimestamp(
        input_file_path.stat().st_ctime
    ) < date.today()


def initialize_table():
    with sqlite3.connect(DATABASES["default"]["NAME"]) as conn:
        CovidDataRaw.objects.all().delete()
        read_covid_data_raw = pd.read_csv(input_file_path)
        read_covid_data_raw.to_sql(
            CovidDataRaw._meta.db_table, conn, index=False, if_exists="append"
        )
        CovidDataClean.objects.all().delete()
        conn.executescript(
            """
            DROP VIEW IF EXISTS COVID_DATA_CLEAN;
            CREATE VIEW COVID_DATA_CLEAN as
            select iso_code,
                   continent,
                   location,
                   date,
                   cast(coalesce(new_cases, 0) as integer) as new_cases,
                   cast(sum(new_cases) over (partition by iso_code rows between unbounded preceding and current row) as integer)
                   as total_cases,
                   coalesce(cast(new_deaths as integer), 0) as new_deaths,
                   sum(new_deaths) over (partition by iso_code rows between unbounded preceding and current row)
                   as total_deaths,
                   coalesce(cast(new_tests as integer), 0) as new_tests,
                   sum(new_tests) over (partition by iso_code rows between unbounded preceding and current row)
                   as total_tests
            from data_coviddataraw
            where iso_code is not null
            order by iso_code, date;
            """
        )
