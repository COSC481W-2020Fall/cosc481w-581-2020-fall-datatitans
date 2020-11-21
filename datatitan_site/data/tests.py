from django.test import TestCase
from data.models import Country
from blog.models import Post, Comment
from data.scripts.generate_graphs import gen_graph
from django.utils import timezone
import pandas as pd
from data.scripts.database_handler import input_file_path, initialize_table
import urllib.request
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import json


# Create your tests here.


class DatabaseTestCase(TestCase):
    fixtures = ["country_data.json"]

    # @classmethod
    # def setUpTestData(cls):
    #     """Initialize the test database, and read the input csv file into a pandas dataframe"""
    #     cls.raw_data: pd.DataFrame = pd.read_csv(
    #         "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    #     )
    #     decimals = {
    #         "stringency_index": 2,
    #         "median_age": 1,
    #         "extreme_poverty": 1,
    #         "diabetes_prevalence": 2,
    #         "life_expectancy": 2,
    #     }
    #     cls.raw_data = (
    #         cls.raw_data.round(decimals=3)
    #         .round(decimals=decimals)
    #         .where(cls.raw_data.notnull(), None)
    #     )
    #     initialize_table()

    # def test_upload(self) -> None:
    #     """Verify that the number of entries in the database match the data pulled from the csv file"""
    #     stored_raw_data = CovidDataRaw.objects.values("iso_code", "date")
    #     self.assertEqual(stored_raw_data.count(), len(self.raw_data), f"Expected number of rows: {len(self.raw_data)}; Actual number of rows: {stored_raw_data.count()}")
    #
    # def test_materialized_views(self) -> None:
    #     """Verify that the materialized views work for the test database"""
    #     clean_data_count = len(self.raw_data.dropna(subset=["iso_code", "continent"]))
    #     stored_clean_data_count = CovidDataClean.objects.count()
    #     self.assertNotEqual(stored_clean_data_count, 0)
    #     self.assertEqual(
    #         stored_clean_data_count,
    #         clean_data_count,
    #         f"Expected number of rows: {clean_data_count}; Actual number of rows: {stored_clean_data_count}",
    #     )

    def test_graph(self) -> None:
        """Verify that the graph generator outputs a graph"""
        result = gen_graph("USA", category="deaths", chart_type="LINE")
        self.assertIs(type(result), dict, "Test failed: output is not a dict.")
        self.assertNotEqual(result, {}, "Test failed: graph was not generated.")

    def test_graph_without_codes(self) -> None:
        """Verify that the graph generator does not output a graph when provided with no countries"""
        result = gen_graph(*[], category="cases", chart_type="LINE")
        self.assertIs(type(result), str, "Test failed: output is not a dict.")
        self.assertEqual(result, {}, "Test failed: graph has been generated.")


class BlogTestCase(TestCase):
    """Rewrite of Ben Potter's test"""

    def setUp(self) -> None:
        """Generate a blog post from a call to a Lorem Ipsum API"""
        self.blog_post = {
            "author": "Marcus Tullius Cicero",
            "title": "Lorem Ipsum",
            "text": urllib.request.urlopen(
                url="https://loripsum.net/api/3/medium/plaintext"
            )
            .read()
            .decode("UTF-8"),
        }
        self.test_post = Post(**self.blog_post)
        self.test_post.save()

    def test_blog(self) -> None:
        """Verify that the contents of the blog post match what was generated"""
        for key, val in self.blog_post.items():
            self.assertEqual(val, self.test_post.__getattribute__(key))


class CommentTestCase(TestCase):
    def setUp(self):
        blog_post = Post.objects.create(
            author="Admin", title="Test Blog", text="This is a piece of blog text"
        )
        Comment.objects.create(
            username="Fred",
            text="I am Mr. Flintstone",
            created_date=timezone.now(),
            blog_id=blog_post.id,
        )

    def test_comment_exists(self):
        comment = Comment.objects.get(username="Fred")

        self.assertEqual(comment.text, "I am Mr. Flintstone")


class TableTestCase(StaticLiveServerTestCase):
    fixtures = ["country_data.json"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        initialize_table()
        cls.selenium = webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_graph_title(self):
        """Checks to make sure the title of the graph matches the expected title."""
        self.selenium.get(self.live_server_url)
        search_box = self.selenium.find_element_by_css_selector("input#country_search")
        country_list = self.selenium.find_element_by_css_selector("ul#id_iso_code")
        search_box.send_keys("united states")
        self.assertEqual(
            len(
                list(
                    filter(
                        lambda x: x.is_displayed(),
                        country_list.find_elements_by_css_selector("ul#id_iso_code>li"),
                    )
                )
            ),
            2,
        )
        country_list.find_element_by_css_selector(
            "input[type='checkbox'][value='USA']"
        ).click()
        self.selenium.find_element_by_css_selector(
            "#country_select_form>button[type='submit']"
        ).click()
        self.selenium.find_element_by_id("graph_data")
        self.assertRegex(
            self.selenium.find_elements_by_css_selector(
                "g.mpld3-baseaxes > text.mpld3-text"
            )[2].text,
            r"^(Total|New)\s(Cases|Deaths|Tests)\s((Per\s(Million|Thousand)\s)|)in\s",
        )
