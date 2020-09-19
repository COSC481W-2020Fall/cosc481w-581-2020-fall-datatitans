from django.conf import settings
from django.db import models
from django.utils import timezone


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


class Post(models.Model):
    author = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


def publish(self):
    self.published_date = timezone.now()
    self.save()


def __str__(self):
    return self.title
