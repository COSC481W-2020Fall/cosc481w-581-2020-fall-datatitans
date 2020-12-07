from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from pathlib import Path
from datatitan_site.settings import BASE_DIR


class Command(BaseCommand):
    help = "Generates a parquet file from the source data."

    def handle(self, *args, **options):
        df = (
            pd.read_csv(
                "https://covid.ourworldindata.org/data/owid-covid-data.csv",
                parse_dates=["date"],
            )
            .sort_values(["iso_code", "date"])
            .astype(
                {
                    "iso_code": "category",
                    "continent": "category",
                    "location": "category",
                    "tests_units": "category",
                }
            )
            .set_index(["iso_code", "date"], drop=False)
        )
        df.to_parquet(BASE_DIR / "data/input/owid-covid-data.parquet")
