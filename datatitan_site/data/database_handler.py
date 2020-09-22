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
                   total_cases,
                   new_cases,
                   new_cases_smoothed,
                   total_deaths,
                   new_deaths,
                   new_deaths_smoothed,
                   total_cases / pop_float * 1000000 as total_cases_per_million,
                   new_cases / pop_float * 1000000 as new_cases_per_million,
                   new_cases_smoothed / pop_float * 1000000 as new_cases_smoothed_per_million,
                   total_deaths / pop_float * 1000000 as total_deaths_per_million,
                   new_deaths / pop_float * 1000000 as new_deaths_per_million,
                   new_deaths_smoothed / pop_float * 1000000 as new_deaths_smoothed_per_million,
                   new_tests,
                   total_tests,
                   total_tests / pop_float * 1000 as total_tests_per_thousand,
                   new_tests / pop_float * 1000 as new_tests_per_thousand,
                   new_tests_smoothed,
                   new_tests_smoothed / pop_float * 1000 as new_tests_smoothed_per_thousand,
                   avg(new_tests / new_cases) over (partition by iso_code rows between 6 preceding and current row)
                       as tests_per_case,
                   avg(new_cases / new_tests) over (partition by iso_code rows between 6 preceding and current row)
                       as positive_rate,
                   tests_units,
                   stringency_index,
                   population
            from (
                select iso_code,
                       continent,
                       location,
                       date,
                       sum(new_cases) over (partition by iso_code rows between unbounded preceding and current row)
                           as total_cases,
                       new_cases,
                       avg(new_cases) over (partition by iso_code rows between 6 preceding and current row)
                           as new_cases_smoothed,
                       sum(new_deaths) over (partition by iso_code rows between unbounded preceding and current row)
                           as total_deaths,
                       new_deaths,
                       avg(new_deaths) over (partition by iso_code rows between 6 preceding and current row)
                           as new_deaths_smoothed,
                       new_tests,
                       sum(new_tests) over (partition by iso_code rows between unbounded preceding and current row)
                           as total_tests,
                       avg(new_tests) over (partition by iso_code rows between 6 preceding and current row)
                           as new_tests_smoothed,
                       tests_units,
                       stringency_index,
                       population,
                       cast(population as real) as pop_float
                from (
                    select iso_code,
                           continent,
                           location,
                           date,
                           coalesce(new_cases, 0) as new_cases,
                           coalesce(new_deaths, 0) as new_deaths,
                           coalesce(new_tests, 0) as new_tests,
                           tests_units,
                           coalesce(stringency_index, 0.0) as stringency_index,
                           population
                    from data_coviddataraw))
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
