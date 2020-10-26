import django
from django.contrib import admin
from data.models import Post
from datatitan_site import settings
import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datatitan_site.settings")
django.setup()

from django.core.management import call_command
DJANGO_SETTINGS_MODULE=datatitan_site.settings
def main():
    author = "Ben Potter"
    title = "Test"
    text = "Please work"
    created_date = datetime.datetime()
    published_date = datetime.datetime()
    Post(author, title, text, created_date, published_date).save()

