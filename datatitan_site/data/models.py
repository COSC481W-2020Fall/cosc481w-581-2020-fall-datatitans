from django.conf import settings
from django.db import models


# Create your models here.
class country(models.Model):
    country_code = models.CharField(max_length=3)
    name = models.CharField(max_length=55)
    continent = models.CharField(max_length=15)
    population = models.IntegerField()


class CovidDataClean(models.Model):
    iso_code = models.CharField(max_length=8, unique_for_date='date')
    continent = models.CharField(max_length=15, unique_for_date='date')
    location = models.CharField(max_length=55, unique_for_date='date')
    date = models.DateField()
    new_cases = models.IntegerField(default=0)
    total_cases = models.IntegerField()
    new_deaths = models.IntegerField(default=0)
    total_deaths = models.IntegerField()
    new_tests = models.IntegerField(default=0)
    total_tests = models.IntegerField()
    # population = models.PositiveIntegerField(default=0)
