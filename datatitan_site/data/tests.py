from django.test import TestCase
from data.models import CovidDataClean, CovidDataRaw
from data.scripts.generate_graphs import gen_graph
import pandas as pd
from data.scripts.database_handler import input_file_path, initialize_table


# Create your tests here.


class DatabaseTestCase(TestCase):
    def setUp(self) -> None:
        self.raw_data = pd.read_csv(input_file_path)
        decimals = {
            "stringency_index": 2,
            "median_age": 1,
            "extreme_poverty": 1,
            "diabetes_prevalence": 2,
            "life_expectancy": 2,
        }
        self.raw_data = (
            self.raw_data.round(decimals=3)
            .round(decimals=decimals)
            .where(self.raw_data.notnull(), None)
        )
        initialize_table()

    def test_upload(self):
        if CovidDataRaw.objects.count() != len(self.raw_data):
            raise AssertionError(
                f"Expected number of rows: {len(self.raw_data)}; Actual number of rows: {CovidDataRaw.objects.count()}"
            )


class GenGraphTest(TestCase):
    def setUP(self):
        self.code=("USA")
        self.graph=("LINE")
        self.type=("TOTAL_DEATHS")

    def test_graph(self):
        result = gen_graph(code, type, graph)
        self.assertEqual(result, "")

    if result.length > 0:
        print("Test passed, graph has been generated.")
    else:
        print("Test failed, graph has not been generated.")
