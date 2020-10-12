#

# %%
from sqlalchemy import create_engine
from datetime import date
from pathlib import Path
import pandas as pd
from django.db.models import Avg, Sum, RowRange, Window, F, FloatField, CharField
from django.db.models.functions import Coalesce, Cast, Concat, TruncMonth
from datatitan_site.settings import DATABASES, BASE_DIR
from data.models import CovidDataRaw, CovidDataClean, Country, Months, CovidDataMonthly

# %%
input_file_path = Path(__file__).parent.parent / "input" / "owid-covid-data.csv"

# %%
engine = create_engine(
    f'sqlite:///{DATABASES["default"]["NAME"].relative_to(BASE_DIR)}'
)


# %%
def input_missing_or_outdated() -> bool:
    """Check to see if the input file is missing or outdated

    :returns: True if input file does not exist, or was not created today.
    """
    return (not input_file_path.exists()) or date.fromtimestamp(
        input_file_path.stat().st_ctime
    ) < date.today()


# %%
def initialize_table() -> None:
    """Replace the raw covid data table with a fresh copy, then clean up the data, and generate a table of countries."""
    with engine.connect() as conn:
        read_covid_data_raw = pd.read_csv(
            input_file_path,
            dtype={
                "iso_code": "string",
                "continent": "string",
                "tests_units": "string",
            },
        )
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
            data_key=Concat(Cast(F("date"), CharField()), F("iso_code")),
        )
    )
    # %%
    CovidDataClean.objects.bulk_create(
        [CovidDataClean(**row) for row in clean_data], ignore_conflicts=True
    )
    # %%
    countries = (
        CovidDataRaw.objects.values(
            "continent", "population", country_code=F("iso_code"), name=F("location"),
        ).order_by("iso_code")
        # .filter(iso_code__in=("USA", "CAN", "MEX"))
    )
    Country.objects.all().delete()
    Country.objects.bulk_create(
        [Country(**c) for c in countries.distinct()], ignore_conflicts=True
    )
    # %%
    Months.objects.bulk_create(
        [
            Months(month=month)
            for month in CovidDataClean.objects.dates("date", "month")
        ],
        ignore_conflicts=True,
    )
    # %%
    monthly_data = CovidDataClean.objects.values(
        "iso_code", "continent", "location", month=TruncMonth(F("date"))
    ).annotate(
        new_cases=Window(
            Sum(F("new_cases")), partition_by=[F("iso_code"), TruncMonth(F("date"))]
        ),
        new_deaths=Window(
            Sum(F("new_deaths")), partition_by=[F("iso_code"), TruncMonth(F("date"))]
        ),
        new_tests=Window(
            Sum(F("new_tests")), partition_by=[F("iso_code"), TruncMonth(F("date"))]
        ),
        data_key=Concat(Cast(TruncMonth(F("date")), CharField()), F("iso_code")),
    ).order_by("iso_code", "month").distinct()
    # %%
    CovidDataMonthly.objects.bulk_create(
        [
            CovidDataMonthly(
                month=Months.objects.get(month=row["month"]),
                **{k: v for k, v in row.items() if k != "month"},
            )
            for row in monthly_data
        ],
        ignore_conflicts=True,
    )
