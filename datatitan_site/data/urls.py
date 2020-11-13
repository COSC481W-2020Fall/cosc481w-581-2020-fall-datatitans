from django.urls import path

import blog.views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', blog.views.blog, name='blog'),
    path('blog_detail/<blog_id>', blog.views.blog_detail, name='blog_detail'),
]
