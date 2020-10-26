from django.test import TestCase
from data.models import CovidDataRaw, Post
from data.scripts.generate_graphs import gen_graph
import pandas as pd
from data.scripts.database_handler import input_file_path, initialize_table
import urllib.request


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

    def test_graph(self) -> None:
        """Verify that the graph generator outputs a graph"""
        result = gen_graph("USA", category="total_deaths", chart_type="LINE")
        self.assertIs(type(result), str, "Test failed: output is not a string.")
        self.assertNotEqual(result, "", "Test failed: graph was not generated.")

    def test_graph_without_codes(self) -> None:
        result = gen_graph(*[], category="total_cases", chart_type="LINE")
        self.assertIs(type(result), str, "Test failed: output is not a string.")
        self.assertEqual(result, "", "Test failed: graph has been generated.")





    if result.length > 0:
        print("Test passed, graph has been generated.")
    else:
        print("Test failed, graph has not been generated.")
