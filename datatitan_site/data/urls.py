from django.urls import path
from . import views, database_handler
import urllib.request
from .models import CovidDataRaw

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog_detail/<blog_id>', views.blog_detail, name='blog_detail'),
]

#if database_handler.input_missing_or_outdated():
#    urllib.request.urlretrieve(url="https://covid.ourworldindata.org/data/owid-covid-data.csv",
#                               filename=database_handler.input_file_path)
#    database_handler.initialize_table()
#elif not CovidDataRaw.objects.exists():
#    database_handler.initialize_table()