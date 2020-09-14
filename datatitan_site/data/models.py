from django.conf import settings
from django.db import models

# Create your models here.
class country(models.Model):
    country_code = models.CharField(max_length=3)
    name = models.CharField(max_length=55)
    continent = models.CharField(max_length=15)
    population = models.IntegerField()
