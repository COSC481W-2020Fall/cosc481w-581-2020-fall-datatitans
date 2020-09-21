from pathlib import Path
import pandas as pd
import sqlite3
from datatitan_site.settings import DATABASES
from datetime import date
from .models import CovidDataRaw, CovidDataClean


input_file_path = Path(__file__).parent / "input" / "owid-covid-data.csv"
# database_path = Path(__file__).parent / "database" / "test_database.db"


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
                   coalesce(new_cases, 0) as new_cases,
                   sum(coalesce(new_cases, 0)) over (partition by iso_code rows between unbounded preceding and current row)
                   as total_cases,
                   coalesce(new_deaths, 0) as new_deaths,
                   sum(coalesce(new_deaths, 0)) over (partition by iso_code rows between unbounded preceding and current row)
                   as total_deaths,
                   coalesce(new_tests, 0) as new_tests,
                   sum(coalesce(new_tests, 0)) over (partition by iso_code rows between unbounded preceding and current row)
                   as total_tests
            from data_coviddataraw
            where iso_code is not null
            order by iso_code, date;
            """
        )
        pd.read_sql_query(
            """
            select iso_code,
                   continent,
                   location,
                   date,
                   coalesce(new_cases, 0) as new_cases,
                   sum(coalesce(new_cases, 0)) over (partition by iso_code rows between unbounded preceding and current row)
                   as total_cases,
                   coalesce(new_deaths, 0) as new_deaths,
                   sum(coalesce(new_deaths, 0)) over (partition by iso_code rows between unbounded preceding and current row)
                   as total_deaths,
                   coalesce(new_tests, 0) as new_tests,
                   sum(coalesce(new_tests, 0)) over (partition by iso_code rows between unbounded preceding and current row)
                   as total_tests
            from data_coviddataraw
            where iso_code is not null and continent is not null
            order by iso_code, date;
            """,
            con=conn,
        ).to_sql(CovidDataClean._meta.db_table, con=conn, index=False, if_exists="append")
