from pathlib import Path
import pandas as pd
import sqlite3
from datatitan_site.settings import DATABASES
from datetime import date
from .models import CovidDataRaw, CovidDataClean, Country


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
        pd.read_sql_query(
            """
            select iso_code,
                   continent,
                   location,
                   date,
                   new_cases,
                   sum(new_cases) over (partition by iso_code rows between unbounded preceding and current row)
                   as total_cases,
                   avg(new_cases) over (partition by iso_code rows between 7 preceding and current row)
                   as new_cases_smoothed,
                   new_deaths,
                   sum(new_deaths) over (partition by iso_code rows between unbounded preceding and current row)
                   as total_deaths,
                   avg(new_deaths) over (partition by iso_code rows between 7 preceding and current row)
                   as new_deaths_smoothed,
                   new_tests,
                   sum(new_tests) over (partition by iso_code rows between unbounded preceding and current row)
                   as total_tests,
                   avg(new_tests) over (partition by iso_code rows between 7 preceding and current row)
                   as new_tests_smoothed
            from (
            select iso_code,
            continent,
            location,
            date,
            coalesce(new_cases, 0) as new_cases,
            coalesce(new_deaths, 0) as new_deaths,
            coalesce(new_tests, 0) as new_tests
            from data_coviddataraw)
            where iso_code is not null and continent is not null
            order by iso_code, date;
            """,
            con=conn,
        ).to_sql(
            CovidDataClean._meta.db_table, con=conn, index=False, if_exists="append"
        )
        Country.objects.all().delete()
        pd.read_sql_query(
            """
            select iso_code as country_code,
            location as name,
            continent,
            population
            from data_coviddataraw
            where iso_code in ('USA', 'CAN', 'MEX')
            group by iso_code
            """,
            con=conn,
        ).to_sql(Country._meta.db_table, con=conn, index=False, if_exists="append")
