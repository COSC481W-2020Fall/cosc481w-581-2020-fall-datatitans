from django.apps import AppConfig
import sys
import urllib.request


class DataConfig(AppConfig):
    name = 'data'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        from .database_handler import input_missing_or_outdated, input_file_path, initialize_table
        from .models import CovidDataRaw
        if input_missing_or_outdated():
            urllib.request.urlretrieve(url="https://covid.ourworldindata.org/data/owid-covid-data.csv",
                                       filename=input_file_path)
            initialize_table()
        elif not CovidDataRaw.objects.exists():
            initialize_table()
