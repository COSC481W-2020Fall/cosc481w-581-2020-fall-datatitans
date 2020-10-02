# %%
from sqlalchemy import create_engine
from datetime import date
from pathlib import Path
import pandas as pd
from django.db.models import (
    Avg,
    Sum,
    RowRange,
    Window,
    F,
    FloatField,
)
from django.db.models.functions import Coalesce, Cast
from datatitan_site.settings import DATABASES, BASE_DIR
from data.models import CovidDataRaw, CovidDataClean, Country

# %%
input_file_path = Path(__file__).parent / "input" / "owid-covid-data.csv"
# database_path = Path(__file__).parent / "database" / "test_database.db"

# %%
engine = create_engine(
    f'sqlite:///{DATABASES["default"]["NAME"].relative_to(BASE_DIR)}'
)

def input_missing_or_outdated():
    return (not input_file_path.exists()) or date.fromtimestamp(
        input_file_path.stat().st_ctime
    ) < date.today()


def initialize_table():
    with engine.connect() as conn:
        read_covid_data_raw = pd.read_csv(input_file_path)
        read_covid_data_raw.round(decimals=3).to_sql(
            CovidDataRaw._meta.db_table, conn, index=False, if_exists="replace"
        )
    # %%
    window = {"partition_by": F("iso_code"), "order_by": [F("date")]}
    past_week = RowRange(start=-6, end=0)
    clean_data = (
        CovidDataRaw.objects.exclude(iso_code__isnull=True)
        .values("iso_code", "continent", "location", "date")
        .annotate(
            new_cases=Coalesce(F("new_cases"), 0),
            new_deaths=Coalesce(F("new_deaths"), 0),
            new_tests=Coalesce(F("new_tests"), 0),
        )
        .annotate(
            total_cases=Window(expression=Sum(F("new_cases")), **window),
            new_cases_smoothed=Window(
                expression=Avg(F("new_cases")), frame=past_week, **window
            ),
            total_deaths=Window(expression=Sum(F("new_deaths")), **window),
            new_deaths_smoothed=Window(
                expression=Avg(F("new_deaths")), frame=past_week, **window
            ),
            total_tests=Window(expression=Sum(F("new_tests")), **window),
            new_tests_smoothed=Window(
                expression=Avg(F("new_tests")), frame=past_week, **window
            ),
        )
        .annotate(
            total_cases_per_million=Cast(F("total_cases"), FloatField())
            / Cast(F("population"), FloatField())
            * 1000000,
            new_cases_per_million=Cast(F("new_cases"), FloatField())
            / Cast(F("population"), FloatField())
            * 1000000,
            new_cases_smoothed_per_million=F("new_cases_smoothed")
            / Cast(F("population"), FloatField())
            * 1000000,
            total_deaths_per_million=Cast(F("total_deaths"), FloatField())
            / Cast(F("population"), FloatField())
            * 1000000,
            new_deaths_per_million=Cast(F("new_deaths"), FloatField())
            / Cast(F("population"), FloatField())
            * 1000000,
            new_deaths_smoothed_per_million=F("new_deaths_smoothed")
            / Cast(F("population"), FloatField())
            * 1000000,
            total_tests_per_thousand=Cast(F("total_tests"), FloatField())
            / Cast(F("population"), FloatField())
            * 1000,
            new_tests_per_thousand=Cast(F("new_tests"), FloatField())
            / Cast(F("population"), FloatField())
            * 1000,
            new_tests_smoothed_per_thousand=F("new_tests_smoothed")
            / Cast(F("population"), FloatField())
            * 1000,
            tests_per_case=Window(
                expression=Avg(
                    Cast(F("new_tests"), FloatField())
                    / Cast(F("new_cases"), FloatField())
                ),
                frame=past_week,
                **window,
            ),
            positive_rate=Window(
                expression=Avg(
                    Cast(F("new_cases"), FloatField())
                    / Cast(F("new_tests"), FloatField())
                ),
                frame=past_week,
                **window,
            ),
        )
        .annotate(
            tests_units=F("tests_units"),
            stringency_index=F("stringency_index"),
            population=F("population"),
        )
    )
    # %%
    # pd.read_sql_query(
    #     """
    #     select iso_code,
    #            continent,
    #            location,
    #            date,
    #            total_cases,
    #            new_cases,
    #            new_cases_smoothed,
    #            total_deaths,
    #            new_deaths,
    #            new_deaths_smoothed,
    #            total_cases / pop_float * 1000000 as total_cases_per_million,
    #            new_cases / pop_float * 1000000 as new_cases_per_million,
    #            new_cases_smoothed / pop_float * 1000000 as new_cases_smoothed_per_million,
    #            total_deaths / pop_float * 1000000 as total_deaths_per_million,
    #            new_deaths / pop_float * 1000000 as new_deaths_per_million,
    #            new_deaths_smoothed / pop_float * 1000000 as new_deaths_smoothed_per_million,
    #            new_tests,
    #            total_tests,
    #            total_tests / pop_float * 1000 as total_tests_per_thousand,
    #            new_tests / pop_float * 1000 as new_tests_per_thousand,
    #            new_tests_smoothed,
    #            new_tests_smoothed / pop_float * 1000 as new_tests_smoothed_per_thousand,
    #            avg(new_tests / new_cases) over (partition by iso_code rows between 6 preceding and current row)
    #                as tests_per_case,
    #            avg(new_cases / new_tests) over (partition by iso_code rows between 6 preceding and current row)
    #                as positive_rate,
    #            tests_units,
    #            stringency_index,
    #            population
    #     from (
    #         select iso_code,
    #                continent,
    #                location,
    #                date,
    #                sum(new_cases) over (partition by iso_code rows between unbounded preceding and current row)
    #                    as total_cases,
    #                new_cases,
    #                avg(new_cases) over (partition by iso_code rows between 6 preceding and current row)
    #                    as new_cases_smoothed,
    #                sum(new_deaths) over (partition by iso_code rows between unbounded preceding and current row)
    #                    as total_deaths,
    #                new_deaths,
    #                avg(new_deaths) over (partition by iso_code rows between 6 preceding and current row)
    #                    as new_deaths_smoothed,
    #                new_tests,
    #                sum(new_tests) over (partition by iso_code rows between unbounded preceding and current row)
    #                    as total_tests,
    #                avg(new_tests) over (partition by iso_code rows between 6 preceding and current row)
    #                    as new_tests_smoothed,
    #                tests_units,
    #                stringency_index,
    #                population,
    #                cast(population as real) as pop_float
    #         from (
    #             select iso_code,
    #                    continent,
    #                    location,
    #                    date,
    #                    coalesce(new_cases, 0) as new_cases,
    #                    coalesce(new_deaths, 0) as new_deaths,
    #                    coalesce(new_tests, 0) as new_tests,
    #                    tests_units,
    #                    coalesce(stringency_index, 0.0) as stringency_index,
    #                    population
    #             from data_coviddataraw))
    #     where iso_code is not null and continent is not null
    #     order by iso_code, date;
    #     """,
    #     con=conn,
    # ).to_sql(
    #     CovidDataClean._meta.db_table, con=conn, index=False, if_exists="append"
    # )
    # %%
    CovidDataClean.objects.bulk_create(
        [CovidDataClean(**row) for row in clean_data], ignore_conflicts=True
    )
    # Country.objects.all().delete()
    # pd.read_sql_query(
    #     """
    #     select iso_code as country_code,
    #     location as name,
    #     continent,
    #     population
    #     from data_coviddataraw
    #     where iso_code in ('USA', 'CAN', 'MEX')
    #     group by iso_code
    #     """,
    #     con=conn,
    # ).to_sql(Country._meta.db_table, con=conn, index=False, if_exists="append")
    countries = (
        CovidDataRaw.objects.values(
            "continent", "population", country_code=F("iso_code"), name=F("location"),
        )
        .order_by("iso_code")
        .filter(iso_code__in=("USA", "CAN", "MEX"))
    )
    Country.objects.all().delete()
    Country.objects.bulk_create(
        [Country(**c) for c in countries.distinct()], ignore_conflicts=True
    )
