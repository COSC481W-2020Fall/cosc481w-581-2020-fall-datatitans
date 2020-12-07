#

# %%
from datetime import date
from pathlib import Path
import pandas as pd
from django.db.models import Avg, Sum, RowRange, Window, F, FloatField, CharField
from django.db.models.functions import Coalesce, Cast, Concat, TruncMonth
from data.models import Country, CountryStats
from django.db import connections, transaction
from backoff import on_exception, expo
from django.db.utils import OperationalError
import os

# %%
input_file_path = Path(__file__).parent.parent / "input" / "owid-covid-data.csv"


# %%
def input_missing_or_outdated() -> bool:
    """Check to see if the input file is missing or outdated

    :returns: True if input file does not exist, or was not created today.
    """
    return (not input_file_path.exists()) or date.fromtimestamp(
        input_file_path.stat().st_ctime
    ) < date.today()


database = connections["default"]


# %%
@on_exception(
    wait_gen=expo, exception=OperationalError, max_tries=8, max_time=120, max_value=16
)
@transaction.atomic()
def initialize_table() -> None:
    """Update the raw covid data table with data retrieved from the "Our World in Data" repository."""
    database.ensure_connection()
    # read_covid_data_raw = (
    #     pd.read_csv(
    #         "https://covid.ourworldindata.org/data/owid-covid-data.csv",
    #         usecols=[
    #             "iso_code",
    #             "continent",
    #             "location",
    #             "new_cases",
    #             "new_deaths",
    #             "new_tests",
    #         ],
    #     )
    #     .round(decimals=3)
    #     .round(
    #         decimals={
    #             "stringency_index": 2,
    #             "median_age": 1,
    #             "extreme_poverty": 1,
    #             "diabetes_prevalence": 2,
    #             "life_expectancy": 2,
    #         }
    #     )
    # )
    # %%
    raw_data = (
        pd.read_csv(
            "https://covid.ourworldindata.org/data/owid-covid-data.csv",
            usecols=[
                "iso_code",
                "continent",
                "location",
                "date",
                "population",
                "new_cases",
                "new_deaths",
                "new_tests",
            ],
        )
        .dropna(subset=["iso_code", "continent", "location", "population"])
        .set_index(["iso_code", "date"])
        .sort_index()
    )
    # %%
    country_aggregates = (
        raw_data[["new_cases", "new_deaths", "new_tests"]]
        # .reset_index()
        .groupby([pd.Grouper(level="iso_code")]).agg(
            total_cases=pd.NamedAgg("new_cases", "sum"),
            total_deaths=pd.NamedAgg("new_deaths", "sum"),
            total_tests=pd.NamedAgg("new_tests", "sum"),
        )
    )
    # %%
    country_facts = (
        raw_data[["continent", "location", "population"]]
        # .set_index("iso_code")
        .drop_duplicates().rename(columns={"location": "name"})
    )
    # %%
    # read_covid_data_raw: pd.DataFrame = read_covid_data_raw.where(
    #     read_covid_data_raw.notnull(), None
    # )
    # read_covid_data_raw["data_key"] = read_covid_data_raw.apply(
    #     lambda row: f"{str(row.date)}{str(row.iso_code)}", axis=1
    # )
    # valid_columns = [field.name for field in Country._meta.get_fields()]
    # valid_columns.remove("id")
    Country.objects.bulk_create(
        [
            Country(**row)
            for row in country_facts.reset_index()
            .drop(columns=["date"])
            .to_dict("records")
        ],
        ignore_conflicts=True,
    )
    CountryStats.objects.all().delete()
    CountryStats.objects.bulk_create(
        [
            CountryStats(iso_code_id=key, **val)
            for key, val in country_aggregates.to_dict("index").items()
        ],
        ignore_conflicts=True,
    )
    # refresh()
    # # %%
    # window = {"partition_by": F("iso_code"), "order_by": [F("date")]}
    # past_week = RowRange(start=-6, end=0)
    # clean_data = (
    #     CovidDataRaw.objects.exclude(iso_code__isnull=True)
    #     .values("iso_code", "continent", "location", "date")
    #     .annotate(
    #         new_cases=Coalesce(F("new_cases"), 0),
    #         new_deaths=Coalesce(F("new_deaths"), 0),
    #         new_tests=Coalesce(F("new_tests"), 0),
    #     )
    #     .annotate(
    #         total_cases=Window(expression=Sum(F("new_cases")), **window),
    #         new_cases_smoothed=Window(
    #             expression=Avg(F("new_cases")), frame=past_week, **window
    #         ),
    #         total_deaths=Window(expression=Sum(F("new_deaths")), **window),
    #         new_deaths_smoothed=Window(
    #             expression=Avg(F("new_deaths")), frame=past_week, **window
    #         ),
    #         total_tests=Window(expression=Sum(F("new_tests")), **window),
    #         new_tests_smoothed=Window(
    #             expression=Avg(F("new_tests")), frame=past_week, **window
    #         ),
    #     )
    #     .annotate(
    #         total_cases_per_million=Cast(F("total_cases"), FloatField())
    #         / Cast(F("population"), FloatField())
    #         * 1000000,
    #         new_cases_per_million=Cast(F("new_cases"), FloatField())
    #         / Cast(F("population"), FloatField())
    #         * 1000000,
    #         new_cases_smoothed_per_million=F("new_cases_smoothed")
    #         / Cast(F("population"), FloatField())
    #         * 1000000,
    #         total_deaths_per_million=Cast(F("total_deaths"), FloatField())
    #         / Cast(F("population"), FloatField())
    #         * 1000000,
    #         new_deaths_per_million=Cast(F("new_deaths"), FloatField())
    #         / Cast(F("population"), FloatField())
    #         * 1000000,
    #         new_deaths_smoothed_per_million=F("new_deaths_smoothed")
    #         / Cast(F("population"), FloatField())
    #         * 1000000,
    #         total_tests_per_thousand=Cast(F("total_tests"), FloatField())
    #         / Cast(F("population"), FloatField())
    #         * 1000,
    #         new_tests_per_thousand=Cast(F("new_tests"), FloatField())
    #         / Cast(F("population"), FloatField())
    #         * 1000,
    #         new_tests_smoothed_per_thousand=F("new_tests_smoothed")
    #         / Cast(F("population"), FloatField())
    #         * 1000,
    #         tests_per_case=Window(
    #             expression=Avg(
    #                 Cast(F("new_tests"), FloatField())
    #                 / Cast(F("new_cases"), FloatField())
    #             ),
    #             frame=past_week,
    #             **window,
    #         ),
    #         positive_rate=Window(
    #             expression=Avg(
    #                 Cast(F("new_cases"), FloatField())
    #                 / Cast(F("new_tests"), FloatField())
    #             ),
    #             frame=past_week,
    #             **window,
    #         ),
    #     )
    #     .annotate(
    #         tests_units=F("tests_units"),
    #         stringency_index=F("stringency_index"),
    #         population=F("population"),
    #         data_key=Concat(Cast(F("date"), CharField()), F("iso_code")),
    #     )
    # )
    # # %%
    # CovidDataClean.objects.bulk_create(
    #     [CovidDataClean(**row) for row in clean_data], ignore_conflicts=True
    # )
    # # %%
    # countries = (
    #     CovidDataRaw.objects.values(
    #         "continent", "population", iso_code=F("iso_code"), name=F("location"),
    #     ).order_by("iso_code")
    #     # .filter(iso_code__in=("USA", "CAN", "MEX"))
    # )
    # # Country.objects.all().delete()
    # Country.objects.bulk_create(
    #     [Country(**c) for c in countries.distinct()], ignore_conflicts=True
    # )
    # # %%
    # Months.objects.bulk_create(
    #     [
    #         Months(month=month)
    #         for month in CovidDataClean.objects.dates("date", "month")
    #     ],
    #     ignore_conflicts=True,
    # )
    # # %%
    # monthly_data = (
    #     CovidDataClean.objects.values(
    #         "iso_code", "continent", "location", month=TruncMonth(F("date"))
    #     )
    #     .annotate(
    #         new_cases=Window(
    #             Sum(F("new_cases")), partition_by=[F("iso_code"), TruncMonth(F("date"))]
    #         ),
    #         new_deaths=Window(
    #             Sum(F("new_deaths")),
    #             partition_by=[F("iso_code"), TruncMonth(F("date"))],
    #         ),
    #         new_tests=Window(
    #             Sum(F("new_tests")), partition_by=[F("iso_code"), TruncMonth(F("date"))]
    #         ),
    #         data_key=Concat(Cast(TruncMonth(F("date")), CharField()), F("iso_code")),
    #     )
    #     .order_by("iso_code", "month")
    #     .distinct()
    # )
    # # %%
    # CovidDataMonthly.objects.bulk_create(
    #     [
    #         CovidDataMonthly(
    #             month=Months.objects.get(month=row["month"]),
    #             **{k: v for k, v in row.items() if k != "month"},
    #         )
    #         for row in monthly_data
    #     ],
    #     ignore_conflicts=True,
    # )


@transaction.atomic()
def refresh():
    with database.cursor() as cursor:
        cursor.execute(
            """
            REFRESH MATERIALIZED VIEW data_coviddataclean;
            REFRESH MATERIALIZED VIEW data_country;
            REFRESH MATERIALIZED VIEW data_months;
            REFRESH MATERIALIZED VIEW data_coviddatamonthly;
            """
        )
