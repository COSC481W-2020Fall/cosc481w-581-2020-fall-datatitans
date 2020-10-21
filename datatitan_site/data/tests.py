from django.test import TestCase
from data.models import CovidDataClean, CovidDataRaw
import pandas as pd
from data.scripts.database_handler import input_file_path


# Create your tests here.


class DatabaseTestCase(TestCase):
    def setUp(self) -> None:
        self.raw_data = pd.read_csv(
            input_file_path,
            # dtype={
            #     "iso_code": "string",
            #     "continent": "string",
            #     "tests_units": "string",
            # },
        )
        decimals = {
            "stringency_index": 2,
            "median_age": 1,
            "extreme_poverty": 1,
            "diabetes_prevalence": 2,
            "life_expectancy": 2
        }
        self.raw_data = self.raw_data.round(decimals=3).round(decimals=decimals).where(self.raw_data.notnull(), None)

    def test_upload(self):
        CovidDataRaw.objects.bulk_create(
            [CovidDataRaw(**row) for row in self.raw_data.to_dict("records")], ignore_conflicts=True, batch_size=1000
        )
        print(CovidDataRaw.objects.count())
        if CovidDataRaw.objects.count() != len(self.raw_data):
            raise AssertionError(f"Expected number of rows: {len(self.raw_data)}; Actual number of rows: {CovidDataRaw.objects.count()}")
