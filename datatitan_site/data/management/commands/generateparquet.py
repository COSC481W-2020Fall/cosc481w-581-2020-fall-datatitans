from django.core.management.base import BaseCommand, CommandError
from datatitan_site.settings import BASE_DIR
import dask.dataframe as dd


class Command(BaseCommand):
    help = "Generates a parquet file from the source data."

    def handle(self, *args, **options):
        ddf: dd.DataFrame = (
            dd.read_csv(
                "https://covid.ourworldindata.org/data/owid-covid-data.csv",
                parse_dates=["date"],
                dtype={"tests_units": "object"},
            )
            .dropna(subset=["iso_code", "continent"])
            .set_index("date")
        )
        ddf.to_parquet(
            BASE_DIR / "data/input/owid-covid-data",
            engine="pyarrow",
            overwrite=True,
            partition_on=["continent", "iso_code"],
        )
