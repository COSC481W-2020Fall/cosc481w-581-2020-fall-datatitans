from django.urls import path

import blog.views
from data import views

urlpatterns = [
    path("", views.data, name="data"),
    path("testing_map/", views.testing_map, name="testing_map"),
    # path('about/', views.about, name='about'),
    # path('blog/', blog.views.blog, name='blog'),
    # path('blog_detail/<blog_id>', blog.views.blog_detail, name='blog_detail'),
]
